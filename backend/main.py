"""
FastAPI Backend for AI Code Explainer
Provides REST API endpoint for code explanation using LLaMA 3.3 70B via Groq
Phase 2: Added RAG (Retrieval-Augmented Generation) support
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging

from groq_integration import get_code_explanation, test_groq_connection
# Lazy imports to avoid startup hang
# from rag_system import get_rag_system
# from fine_tuning import build_few_shot_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Explainer API",
    description="API for explaining code using LLaMA 3.3 70B Versatile with RAG",
    version="2.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class CodeExplanationRequest(BaseModel):
    """Request model for code explanation"""
    code: str = Field(..., description="Code snippet to explain", min_length=1, max_length=10000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
            }
        }


class CodeExplanationResponse(BaseModel):
    """Response model for code explanation"""
    explanation: str = Field(..., description="AI-generated explanation of the code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "explanation": "This code implements a recursive Fibonacci function..."
            }
        }


class RAGExplanationResponse(BaseModel):
    """Response model for RAG-enhanced code explanation"""
    explanation: str = Field(..., description="AI-generated explanation with RAG context")
    retrieved_examples: Optional[List[Dict]] = Field(None, description="Retrieved similar examples")
    
    class Config:
        json_schema_extra = {
            "example": {
                "explanation": "This code implements...",
                "retrieved_examples": [
                    {
                        "language": "python",
                        "category": "algorithms",
                        "relevance_score": 0.85
                    }
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "AI Code Explainer API",
        "version": "2.0.0",
        "status": "running",
        "phase": "2",
        "features": ["basic-explanation", "rag-enhanced-explanation", "few-shot-learning"],
        "endpoints": {
            "explain": "/api/explain (POST) - Basic explanation",
            "explain_rag": "/api/explain-rag (POST) - RAG-enhanced explanation",
            "health": "/health (GET)",
            "rag_stats": "/api/rag/stats (GET)",
            "docs": "/docs (GET)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    groq_status = test_groq_connection()
    
    return {
        "status": "healthy" if groq_status else "degraded",
        "groq_api": "connected" if groq_status else "disconnected",
        "model": "llama-3.3-70b-versatile"
    }


@app.post("/api/explain", response_model=CodeExplanationResponse)
async def explain_code(request: CodeExplanationRequest):
    """
    Explain code using LLaMA 3.3 70B Versatile (Basic Mode - Phase 1).
    
    Takes a code snippet and returns a comprehensive explanation.
    """
    try:
        logger.info(f"Received code explanation request (length: {len(request.code)} chars)")
        
        # Get explanation from Groq API
        result = await get_code_explanation(request.code)
        
        if result["success"]:
            logger.info("Successfully generated explanation")
            return CodeExplanationResponse(explanation=result["explanation"])
        else:
            logger.error(f"Failed to generate explanation: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to generate explanation")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/api/explain-rag", response_model=RAGExplanationResponse)
async def explain_code_rag(request: CodeExplanationRequest):
    """
    Explain code using RAG-enhanced LLaMA 3.3 70B Versatile (Phase 2).
    
    Uses Retrieval-Augmented Generation with ChromaDB to find similar code examples,
    applies few-shot learning, and generates higher-quality explanations.
    
    Features:
    - Semantic search for similar code examples
    - Domain-specific prompt engineering
    - Few-shot learning with curated examples
    - Enhanced context awareness
    """
    try:
        # Lazy import to avoid startup hang
        from rag_system import get_rag_system
        from fine_tuning import build_few_shot_prompt
        
        logger.info(f"Received RAG explanation request (length: {len(request.code)} chars)")
        
        # Initialize RAG system
        rag = get_rag_system()
        
        # Retrieve similar code examples from ChromaDB
        logger.info("Retrieving similar code examples from vector database...")
        retrieved_docs = rag.retrieve(
            query_code=request.code,
            top_k=3,
            min_relevance=0.65
        )
        
        logger.info(f"Retrieved {len(retrieved_docs)} relevant examples")
        
        # Build RAG-enhanced prompt with retrieved context
        rag_prompt = rag.build_rag_prompt(
            query_code=request.code,
            retrieved_examples=retrieved_docs
        )
        
        # Build few-shot prompt with domain-specific examples
        few_shot_prompt = build_few_shot_prompt(request.code)
        
        # Combine RAG context with few-shot learning
        combined_prompt = f"""{few_shot_prompt}

## Retrieved Similar Examples for Context:
{rag_prompt if retrieved_docs else "No highly relevant examples found in database."}

## Code to Explain:
```
{request.code}
```

Provide a comprehensive explanation following the structure shown in the examples above."""
        
        # Call LLaMA with enhanced prompt
        logger.info("Generating explanation with RAG-enhanced prompt...")
        result = await get_code_explanation(
            code=request.code,
            custom_prompt=combined_prompt,
            use_rag=True
        )
        
        if result["success"]:
            logger.info("Successfully generated RAG-enhanced explanation")
            
            # Format retrieved examples for response
            retrieved_examples = [
                {
                    "language": doc["metadata"].get("language", "unknown"),
                    "category": doc["metadata"].get("category", "general"),
                    "subcategory": doc["metadata"].get("subcategory", ""),
                    "difficulty": doc["metadata"].get("difficulty", "medium"),
                    "relevance_score": round(doc["relevance_score"], 3)
                }
                for doc in retrieved_docs
            ]
            
            return RAGExplanationResponse(
                explanation=result["explanation"],
                retrieved_examples=retrieved_examples if retrieved_examples else None
            )
        else:
            logger.error(f"Failed to generate RAG explanation: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Failed to generate RAG explanation")
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in RAG endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/rag/stats")
async def rag_statistics():
    """
    Get statistics about the RAG system's document collection.
    
    Returns information about indexed documents, languages, and categories.
    """
    try:
        # Lazy import to avoid startup hang
        from rag_system import get_rag_system
        
        rag = get_rag_system()
        collection = rag.collection
        
        # Get total document count
        total_docs = collection.count()
        
        # Get sample documents to analyze metadata
        if total_docs > 0:
            results = collection.get(limit=total_docs)
            
            # Analyze metadata
            languages = {}
            categories = {}
            difficulties = {}
            
            for metadata in results.get("metadatas", []):
                lang = metadata.get("language", "unknown")
                cat = metadata.get("category", "general")
                diff = metadata.get("difficulty", "medium")
                
                languages[lang] = languages.get(lang, 0) + 1
                categories[cat] = categories.get(cat, 0) + 1
                difficulties[diff] = difficulties.get(diff, 0) + 1
            
            return {
                "total_documents": total_docs,
                "languages": languages,
                "categories": categories,
                "difficulties": difficulties,
                "embedding_dimension": 384,
                "model": "sentence-transformers/all-MiniLM-L6-v2"
            }
        else:
            return {
                "total_documents": 0,
                "message": "No documents indexed yet. Run ingest_documents.py to populate the database."
            }
            
    except Exception as e:
        logger.error(f"Error getting RAG stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve RAG statistics: {str(e)}"
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting AI Code Explainer API (Phase 2: RAG-Enhanced)...")
    logger.info("Testing Groq API connection...")
    
    if test_groq_connection():
        logger.info("✓ Groq API connection successful")
    else:
        logger.warning("✗ Groq API connection failed - check your GROQ_API_KEY")
    
    # RAG system uses lazy loading (loads on first use)
    logger.info("✓ RAG system configured (lazy loading - will initialize on first use)")
    logger.info("  RAG endpoint: /api/explain-rag")
    logger.info("  Stats endpoint: /api/rag/stats")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down AI Code Explainer API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
