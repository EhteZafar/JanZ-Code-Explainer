"""
Document Ingestion Script
Populates ChromaDB with curated code-explanation pairs
"""

import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag_system import RAGSystem
from sample_data.dataset import get_dataset, get_dataset_stats
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def ingest_documents(reset_collection: bool = False):
    """
    Ingest sample documents into ChromaDB.
    
    Args:
        reset_collection: If True, clear existing collection first
    """
    logger.info("=" * 70)
    logger.info("STARTING DOCUMENT INGESTION")
    logger.info("=" * 70)
    
    try:
        # Initialize RAG system
        logger.info("\n1. Initializing RAG system...")
        rag = RAGSystem()
        
        # Reset if requested
        if reset_collection:
            logger.info("\n2. Resetting collection (deleting existing documents)...")
            rag.reset_collection()
        
        # Get dataset
        logger.info("\n3. Loading dataset...")
        dataset = get_dataset()
        stats = get_dataset_stats()
        
        logger.info(f"   Loaded {stats['total_examples']} examples")
        logger.info(f"   Languages: {', '.join(stats['languages'].keys())}")
        logger.info(f"   Categories: {', '.join(stats['categories'].keys())}")
        
        # Prepare documents for batch ingestion
        logger.info("\n4. Preparing documents for ingestion...")
        documents = []
        
        for item in dataset:
            doc = {
                'id': item['id'],
                'code': item['code'],
                'explanation': item['explanation'],
                'metadata': {
                    'language': item['language'],
                    'category': item['category'],
                    'subcategory': item.get('subcategory', ''),
                    'difficulty': item.get('difficulty', 'unknown')
                }
            }
            documents.append(doc)
        
        # Ingest in batch
        logger.info(f"\n5. Ingesting {len(documents)} documents into ChromaDB...")
        logger.info("   This may take a minute for embedding generation...")
        
        success = rag.add_documents_batch(documents)
        
        if success:
            logger.info("   ✓ Successfully ingested all documents!")
        else:
            logger.error("   ✗ Failed to ingest documents")
            return False
        
        # Verify ingestion
        logger.info("\n6. Verifying ingestion...")
        stats = rag.get_collection_stats()
        
        logger.info(f"   Collection: {stats['collection_name']}")
        logger.info(f"   Total documents: {stats['total_documents']}")
        logger.info(f"   Embedding model: {stats['embedding_model']}")
        logger.info(f"   Database path: {stats['db_path']}")
        
        if stats['languages']:
            logger.info(f"   Languages in collection:")
            for lang, count in stats['languages'].items():
                logger.info(f"     - {lang}: {count} documents")
        
        # Test retrieval
        logger.info("\n7. Testing retrieval...")
        test_code = "def quicksort(arr): pass"
        results = rag.retrieve(test_code, top_k=3)
        
        if results:
            logger.info(f"   ✓ Retrieval working! Found {len(results)} relevant documents")
            logger.info(f"   Top result: {results[0]['language']} - {results[0]['category']}")
            logger.info(f"   Relevance score: {results[0]['relevance_score']:.3f}")
        else:
            logger.warning("   ⚠ No results found in test retrieval")
        
        logger.info("\n" + "=" * 70)
        logger.info("INGESTION COMPLETE!")
        logger.info("=" * 70)
        logger.info("\nThe RAG system is now ready to use.")
        logger.info("You can test it by running the backend server and using /api/explain-rag endpoint.\n")
        
        return True
        
    except Exception as e:
        logger.error(f"\n✗ Error during ingestion: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_rag_system():
    """Test the RAG system with sample queries."""
    logger.info("\n" + "=" * 70)
    logger.info("TESTING RAG SYSTEM")
    logger.info("=" * 70)
    
    try:
        rag = RAGSystem()
        
        test_queries = [
            ("def binary_search(arr, target): pass", "Binary search algorithm"),
            ("async function fetch(): void {}", "Async function"),
            ("class Singleton { private static instance; }", "Singleton pattern"),
        ]
        
        for code, description in test_queries:
            logger.info(f"\nTest Query: {description}")
            logger.info(f"Code: {code[:50]}...")
            
            results = rag.retrieve(code, top_k=3)
            
            if results:
                logger.info(f"✓ Found {len(results)} results:")
                for i, result in enumerate(results, 1):
                    logger.info(f"  {i}. {result['language']} - {result['category']} "
                              f"(relevance: {result['relevance_score']:.3f})")
            else:
                logger.info("✗ No results found")
        
        logger.info("\n" + "=" * 70)
        logger.info("TESTING COMPLETE")
        logger.info("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"Error during testing: {e}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest documents into ChromaDB for RAG")
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Reset collection (delete existing documents)'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run test queries after ingestion'
    )
    
    args = parser.parse_args()
    
    # Ingest documents
    success = ingest_documents(reset_collection=args.reset)
    
    if not success:
        logger.error("Ingestion failed!")
        sys.exit(1)
    
    # Run tests if requested
    if args.test:
        test_rag_system()


if __name__ == "__main__":
    main()
