"""
RAG (Retrieval-Augmented Generation) System
Implements vector search with ChromaDB for code explanation enhancement
"""

import os
import logging
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from fine_tuning import detect_language

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

# Configuration
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "code_explanations"
RELEVANCE_THRESHOLD = 0.65


class RAGSystem:
    """
    Retrieval-Augmented Generation system for code explanation.
    
    Uses ChromaDB for vector storage and semantic search.
    """
    
    def __init__(self, db_path: str = CHROMA_DB_PATH):
        """
        Initialize RAG system with persistent storage.
        
        Args:
            db_path: Path to ChromaDB storage directory
        """
        self.db_path = db_path
        self.embedding_model = None
        self.client = None
        self.collection = None
        
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB client and load embedding model."""
        try:
            logger.info("Initializing RAG system...")
            
            # Initialize ChromaDB persistent client
            logger.info("Step 1: Creating ChromaDB client...")
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            logger.info("Step 1 complete: ChromaDB client created")
            
            # Get or create collection
            logger.info("Step 2: Getting/creating collection...")
            self.collection = self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={
                    "description": "Code examples with explanations for RAG",
                    "embedding_model": EMBEDDING_MODEL_NAME
                }
            )
            logger.info("Step 2 complete: Collection ready")
            
            # Load embedding model
            logger.info(f"Step 3: Loading embedding model: {EMBEDDING_MODEL_NAME}")
            logger.info("This may take 1-2 minutes on first run (downloading 90MB model)...")
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
            logger.info("Step 3 complete: Embedding model loaded")
            
            # Check collection size
            count = self.collection.count()
            logger.info(f"✓ RAG system initialized. Collection has {count} documents.")
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG system: {e}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text.
        
        Args:
            text: Input text to embed
            
        Returns:
            List of floats representing the embedding
        """
        try:
            embedding = self.embedding_model.encode(
                text,
                convert_to_tensor=False,
                show_progress_bar=False
            )
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []
    
    def add_document(
        self,
        code: str,
        explanation: str,
        metadata: Dict,
        doc_id: Optional[str] = None
    ):
        """
        Add a code-explanation pair to the vector store.
        
        Args:
            code: Source code
            explanation: Explanation of the code
            metadata: Additional metadata (language, category, etc.)
            doc_id: Optional document ID (auto-generated if not provided)
        """
        try:
            # Generate embedding from code
            embedding = self.generate_embedding(code)
            
            if not embedding:
                logger.error("Failed to generate embedding")
                return False
            
            # Generate ID if not provided
            if not doc_id:
                import hashlib
                doc_id = hashlib.md5(code.encode()).hexdigest()[:16]
            
            # Store explanation in metadata
            metadata['explanation'] = explanation
            
            # Add to collection
            self.collection.add(
                embeddings=[embedding],
                documents=[code],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info(f"Added document {doc_id} to collection")
            return True
            
        except Exception as e:
            logger.error(f"Error adding document: {e}")
            return False
    
    def add_documents_batch(self, documents: List[Dict]):
        """
        Add multiple documents in batch.
        
        Args:
            documents: List of dicts with 'code', 'explanation', 'metadata'
        """
        try:
            codes = []
            explanations = []
            metadatas = []
            ids = []
            
            for doc in documents:
                import hashlib
                doc_id = doc.get('id', hashlib.md5(doc['code'].encode()).hexdigest()[:16])
                
                codes.append(doc['code'])
                explanations.append(doc['explanation'])
                
                metadata = doc.get('metadata', {})
                metadata['explanation'] = doc['explanation']
                metadatas.append(metadata)
                
                ids.append(doc_id)
            
            # Generate embeddings in batch
            logger.info(f"Generating embeddings for {len(codes)} documents...")
            embeddings = [self.generate_embedding(code) for code in codes]
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=codes,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"✓ Added {len(documents)} documents to collection")
            return True
            
        except Exception as e:
            logger.error(f"Error in batch add: {e}")
            return False
    
    def retrieve(
        self,
        query_code: str,
        top_k: int = 5,
        language: Optional[str] = None,
        min_relevance: float = RELEVANCE_THRESHOLD
    ) -> List[Dict]:
        """
        Retrieve most relevant code examples.
        
        Args:
            query_code: Code to find similar examples for
            top_k: Number of results to return
            language: Filter by programming language
            min_relevance: Minimum relevance score (0-1)
            
        Returns:
            List of relevant code examples with metadata
        """
        try:
            # Check if collection is empty
            if self.collection.count() == 0:
                logger.warning("Collection is empty. Run ingest_documents.py first.")
                return []
            
            # Generate query embedding
            query_embedding = self.generate_embedding(query_code)
            
            if not query_embedding:
                logger.error("Failed to generate query embedding")
                return []
            
            # Detect language if not provided
            if not language:
                language = detect_language(query_code)
            
            # Build metadata filter
            where_filter = None
            if language and language != "unknown":
                where_filter = {"language": language}
            
            # Query collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k * 2, 20),  # Retrieve more for reranking
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )
            
            # If no results with language filter, try without
            if not results['documents'][0] and where_filter:
                logger.info(f"No results for language '{language}', trying without filter...")
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=min(top_k * 2, 20),
                    include=["documents", "metadatas", "distances"]
                )
            
            # Process and rank results
            ranked_results = self._process_results(
                results,
                query_code,
                language
            )
            
            # Filter by relevance threshold
            filtered_results = [
                r for r in ranked_results
                if r['relevance_score'] >= min_relevance
            ]
            
            logger.info(f"Retrieved {len(filtered_results)} relevant documents (from {len(ranked_results)} candidates)")
            
            return filtered_results[:top_k]
            
        except Exception as e:
            logger.error(f"Error during retrieval: {e}")
            return []
    
    def _process_results(
        self,
        results: Dict,
        query_code: str,
        query_language: str
    ) -> List[Dict]:
        """
        Process and rank retrieval results.
        
        Args:
            results: Raw ChromaDB query results
            query_code: Original query code
            query_language: Detected query language
            
        Returns:
            List of processed and ranked results
        """
        processed = []
        
        # Extract results
        documents = results['documents'][0]
        metadatas = results['metadatas'][0]
        distances = results['distances'][0]
        
        for doc, metadata, distance in zip(documents, metadatas, distances):
            # Calculate relevance score
            relevance_score = self._calculate_relevance(
                query_code,
                doc,
                metadata,
                distance,
                query_language
            )
            
            processed.append({
                "code": doc,
                "explanation": metadata.get("explanation", ""),
                "language": metadata.get("language", "unknown"),
                "category": metadata.get("category", "general"),
                "metadata": metadata,
                "relevance_score": relevance_score,
                "distance": distance
            })
        
        # Sort by relevance score (higher is better)
        processed.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return processed
    
    def _calculate_relevance(
        self,
        query: str,
        doc: str,
        metadata: Dict,
        distance: float,
        query_language: str
    ) -> float:
        """
        Calculate composite relevance score.
        
        Combines:
        - Embedding similarity (1 - distance)
        - Language match bonus
        - Length similarity
        
        Args:
            query: Query code
            doc: Retrieved document
            metadata: Document metadata
            distance: Embedding distance
            query_language: Query programming language
            
        Returns:
            Relevance score (0-1, higher is better)
        """
        # Base similarity (convert distance to similarity)
        similarity = max(0, 1 - distance)
        
        # Language match bonus (+0.2)
        doc_language = metadata.get("language", "")
        lang_bonus = 0.2 if doc_language == query_language else 0
        
        # Length similarity bonus (prefer similar complexity)
        query_lines = len(query.split('\n'))
        doc_lines = len(doc.split('\n'))
        if max(query_lines, doc_lines) > 0:
            length_ratio = min(query_lines, doc_lines) / max(query_lines, doc_lines)
            length_bonus = 0.1 * length_ratio
        else:
            length_bonus = 0
        
        # Combine scores
        total_score = similarity + lang_bonus + length_bonus
        
        # Normalize to 0-1 range
        return min(1.0, total_score)
    
    def build_rag_prompt(
        self,
        query_code: str,
        retrieved_examples: List[Dict],
        max_examples: int = 3
    ) -> str:
        """
        Build augmented prompt with retrieved context.
        
        Args:
            query_code: User's code to explain
            retrieved_examples: Retrieved similar examples
            max_examples: Maximum examples to include
            
        Returns:
            Complete prompt with RAG context
        """
        from fine_tuning import SYSTEM_PROMPT, OUTPUT_FORMAT, detect_language
        
        language = detect_language(query_code)
        
        # Build context section
        if not retrieved_examples:
            context_section = ""
        else:
            context_section = "Here are similar code examples for reference:\n\n"
            
            for i, example in enumerate(retrieved_examples[:max_examples], 1):
                # Truncate explanation if too long
                explanation = example['explanation']
                if len(explanation) > 600:
                    explanation = explanation[:600] + "..."
                
                context_section += f"""Example {i} (Relevance: {example['relevance_score']:.2f}, Language: {example['language']}):

```{example['language']}
{example['code']}
```

Explanation: {explanation}

---

"""
        
        # Build complete prompt
        prompt = f"""{SYSTEM_PROMPT}

{OUTPUT_FORMAT}

{context_section}

Now, explain the following code in detail, using a similar comprehensive style:

```{language if language != 'unknown' else ''}
{query_code}
```

Provide a thorough explanation following the structured format above."""
        
        return prompt
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the vector store."""
        try:
            count = self.collection.count()
            
            # Get sample to analyze languages
            if count > 0:
                sample = self.collection.get(limit=min(count, 100))
                languages = [m.get('language', 'unknown') for m in sample['metadatas']]
                lang_counts = {}
                for lang in languages:
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1
            else:
                lang_counts = {}
            
            return {
                "total_documents": count,
                "languages": lang_counts,
                "collection_name": COLLECTION_NAME,
                "embedding_model": EMBEDDING_MODEL_NAME,
                "db_path": self.db_path
            }
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
    
    def reset_collection(self):
        """Reset (delete) the entire collection. Use with caution!"""
        try:
            self.client.delete_collection(COLLECTION_NAME)
            logger.info(f"Collection '{COLLECTION_NAME}' deleted")
            
            # Recreate empty collection
            self.collection = self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={
                    "description": "Code examples with explanations for RAG",
                    "embedding_model": EMBEDDING_MODEL_NAME
                }
            )
            logger.info("New empty collection created")
            return True
        except Exception as e:
            logger.error(f"Error resetting collection: {e}")
            return False


# Initialize global RAG system instance
_rag_system = None

def get_rag_system() -> RAGSystem:
    """Get or create global RAG system instance."""
    global _rag_system
    if _rag_system is None:
        _rag_system = RAGSystem()
    return _rag_system


# Export main components
__all__ = [
    'RAGSystem',
    'get_rag_system',
    'CHROMA_DB_PATH',
    'COLLECTION_NAME',
    'RELEVANCE_THRESHOLD'
]
