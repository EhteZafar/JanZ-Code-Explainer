"""
FastAPI Backend for AI Code Explainer
Provides REST API endpoint for code explanation using LLaMA 3.3 70B via Groq
Phase 3: Enhanced with performance monitoring, ethical AI safeguards, and comprehensive metrics
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import logging
import time
import json
from datetime import datetime

from groq_integration import get_code_explanation, test_groq_connection
from performance_monitor import get_monitor
from ethical_ai import get_ethical_guard
from chat_history import get_chat_db
# Lazy imports to avoid startup hang
# from rag_system import get_rag_system
# from fine_tuning import build_few_shot_prompt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="JanZ Code Explainer API",
    description="API for explaining code using LLaMA 3.3 70B with RAG, Performance Monitoring, and Ethical AI",
    version="3.0.0"
)

# Configure CORS to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Phase 3 components
performance_monitor = get_monitor()
ethical_guard = get_ethical_guard()
chat_db = get_chat_db()


# Request/Response Models
class CodeExplanationRequest(BaseModel):
    """Request model for code explanation"""
    code: str = Field(..., description="Code snippet to explain", min_length=1, max_length=10000)
    language: str = Field(default="python", description="Programming language of the code")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for chat history")
    
    class Config:
        json_schema_extra = {
            "example": {
                "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
                "language": "python",
                "conversation_id": None
            }
        }


class CodeExplanationResponse(BaseModel):
    """Response model for code explanation"""
    explanation: str = Field(..., description="AI-generated explanation of the code")
    conversation_id: str = Field(..., description="Conversation ID for this exchange")
    
    class Config:
        json_schema_extra = {
            "example": {
                "explanation": "This code implements a recursive Fibonacci function...",
                "conversation_id": "abc-123-def-456"
            }
        }


class RAGExplanationResponse(BaseModel):
    """Response model for RAG-enhanced code explanation"""
    explanation: str = Field(..., description="AI-generated explanation with RAG context")
    conversation_id: str = Field(..., description="Conversation ID for this exchange")
    retrieved_examples: Optional[List[Dict]] = Field(None, description="Retrieved similar examples")
    
    class Config:
        json_schema_extra = {
            "example": {
                "explanation": "This code implements...",
                "conversation_id": "abc-123-def-456",
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
    Explain code using LLaMA 3.3 70B Versatile (Basic Mode - Phase 3 Enhanced).
    
    Takes a code snippet and returns a comprehensive explanation with safety checks.
    Now includes chat history persistence.
    """
    start_time = time.time()
    success = False
    error_msg = None
    conversation_id = request.conversation_id
    
    try:
        logger.info(f"Received code explanation request (length: {len(request.code)} chars)")
        
        # Create new conversation if not provided
        if not conversation_id:
            # Auto-generate title from language
            title = f"Explain {request.language} code"
            conversation_id = chat_db.create_conversation(title=title)
            logger.info(f"Created new conversation: {conversation_id}")
        
        # Save user message to chat history
        chat_db.add_message(
            conversation_id=conversation_id,
            role="user",
            content=request.code,
            code_snippet=request.code,
            language=request.language,
            rag_mode=False,
            retrieved_count=0
        )
        
        # Phase 3: Sanitize code for safety
        sanitized_code, warnings = ethical_guard.sanitize_code(request.code)
        if warnings:
            logger.warning(f"Code sanitization warnings: {warnings}")
        
        # Get explanation from Groq API
        result = await get_code_explanation(sanitized_code if warnings else request.code)
        
        if result["success"]:
            # Phase 3: Validate response quality
            is_valid, validation_msg = ethical_guard.validate_response(result["explanation"])
            if not is_valid:
                logger.warning(f"Response validation warning: {validation_msg}")
            
            logger.info("Successfully generated explanation")
            success = True
            
            # Save assistant response to chat history
            chat_db.add_message(
                conversation_id=conversation_id,
                role="assistant",
                content=result["explanation"],
                language=request.language,
                rag_mode=False,
                retrieved_count=0
            )
            
            response_time = time.time() - start_time
            performance_monitor.record_request(
                mode='basic',
                response_time=response_time,
                success=True,
                code_length=len(request.code),
                retrieved_count=0
            )
            
            return CodeExplanationResponse(
                explanation=result["explanation"],
                conversation_id=conversation_id
            )
        else:
            error_msg = result.get("error", "Failed to generate explanation")
            logger.error(f"Failed to generate explanation: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
            
    except HTTPException: 
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Unexpected error: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {error_msg}")
    finally:
        if not success:
            response_time = time.time() - start_time
            performance_monitor.record_request(
                mode='basic',
                response_time=response_time,
                success=False,
                code_length=len(request.code),
                error=error_msg
            )


@app.post("/api/explain-rag", response_model=RAGExplanationResponse)
async def explain_code_rag(request: CodeExplanationRequest):
    """
    Explain code using RAG-enhanced LLaMA 3.3 70B Versatile (Phase 3 Enhanced).
    
    Uses Retrieval-Augmented Generation with ChromaDB to find similar code examples,
    applies few-shot learning, ethical AI safeguards, and performance monitoring.
    Now includes chat history persistence.
    
    Phase 3 Features:
    - Semantic search for similar code examples
    - Domain-specific prompt engineering
    - Few-shot learning with curated examples
    - Code sanitization and safety checks
    - Response validation
    - Performance tracking
    - Chat history storage
    """
    start_time = time.time()
    success = False
    error_msg = None
    retrieved_count = 0
    conversation_id = request.conversation_id
    
    try:
        # Lazy import to avoid startup hang
        from rag_system import get_rag_system
        from fine_tuning import build_few_shot_prompt
        
        logger.info(f"Received RAG explanation request (length: {len(request.code)} chars)")
        
        # Create new conversation if not provided
        if not conversation_id:
            # Auto-generate title from language
            title = f"Explain {request.language} code (RAG)"
            conversation_id = chat_db.create_conversation(title=title)
            logger.info(f"Created new conversation: {conversation_id}")
        
        # Phase 3: Sanitize code for safety
        sanitized_code, warnings = ethical_guard.sanitize_code(request.code)
        if warnings:
            logger.warning(f"Code sanitization warnings: {warnings}")
        
        code_to_use = sanitized_code if warnings else request.code
        
        # Initialize RAG system
        rag = get_rag_system()
        
        # Retrieve similar code examples from ChromaDB
        logger.info("Retrieving similar code examples from vector database...")
        retrieved_docs = rag.retrieve(
            query_code=code_to_use,
            top_k=3,
            min_relevance=0.65
        )
        
        retrieved_count = len(retrieved_docs)
        logger.info(f"Retrieved {retrieved_count} relevant examples")
        
        # Save user message to chat history with RAG context
        rag_context_json = json.dumps([{
            "language": doc["metadata"].get("language", "unknown"),
            "category": doc["metadata"].get("category", "general"),
            "relevance_score": doc["relevance_score"]
        } for doc in retrieved_docs]) if retrieved_docs else None
        
        chat_db.add_message(
            conversation_id=conversation_id,
            role="user",
            content=request.code,
            code_snippet=request.code,
            language=request.language,
            rag_context=rag_context_json,
            rag_mode=True,
            retrieved_count=retrieved_count
        )
        
        # Build RAG-enhanced prompt with retrieved context
        rag_prompt = rag.build_rag_prompt(
            query_code=code_to_use,
            retrieved_examples=retrieved_docs
        )
        
        # Build few-shot prompt with domain-specific examples
        few_shot_prompt = build_few_shot_prompt(code_to_use)
        
        # Combine RAG context with few-shot learning
        combined_prompt = f"""{few_shot_prompt}

## Retrieved Similar Examples for Context:
{rag_prompt if retrieved_docs else "No highly relevant examples found in database."}

## Code to Explain:
```
{code_to_use}
```

Provide a comprehensive explanation following the structure shown in the examples above."""
        
        # Call LLaMA with enhanced prompt
        logger.info("Generating explanation with RAG-enhanced prompt...")
        result = await get_code_explanation(
            code=code_to_use,
            custom_prompt=combined_prompt,
            use_rag=True
        )
        
        if result["success"]:
            # Phase 3: Validate response quality
            is_valid, validation_msg = ethical_guard.validate_response(result["explanation"])
            if not is_valid:
                logger.warning(f"Response validation warning: {validation_msg}")
            
            logger.info("Successfully generated RAG-enhanced explanation")
            success = True
            
            # Save assistant response to chat history
            chat_db.add_message(
                conversation_id=conversation_id,
                role="assistant",
                content=result["explanation"],
                language=request.language,
                rag_mode=True,
                retrieved_count=retrieved_count
            )
            
            # Record performance metrics
            response_time = time.time() - start_time
            performance_monitor.record_request(
                mode='rag',
                response_time=response_time,
                success=True,
                code_length=len(request.code),
                retrieved_count=retrieved_count
            )
            
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
                conversation_id=conversation_id,
                retrieved_examples=retrieved_examples if retrieved_examples else None
            )
        else:
            error_msg = result.get("error", "Failed to generate RAG explanation")
            logger.error(f"Failed to generate RAG explanation: {error_msg}")
            raise HTTPException(status_code=500, detail=error_msg)
            
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Unexpected error in RAG endpoint: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {error_msg}")
    finally:
        if not success:
            response_time = time.time() - start_time
            performance_monitor.record_request(
                mode='rag',
                response_time=response_time,
                success=False,
                code_length=len(request.code),
                retrieved_count=retrieved_count,
                error=error_msg
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


@app.get("/api/metrics/performance")
async def get_performance_metrics():
    """
    Get comprehensive performance metrics and system statistics.
    Phase 3: Performance monitoring endpoint.
    """
    try:
        stats = performance_monitor.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting performance metrics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve performance metrics: {str(e)}"
        )


@app.get("/api/metrics/history")
async def get_request_history(limit: int = 20):
    """
    Get recent request history with performance data.
    Phase 3: Request history endpoint.
    """
    try:
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        
        history = performance_monitor.get_recent_history(limit)
        return {
            "count": len(history),
            "history": history
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting request history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve request history: {str(e)}"
        )


@app.get("/api/ethics/privacy")
async def get_privacy_info():
    """
    Get privacy policy and data handling information.
    Phase 3: Ethical AI transparency endpoint.
    """
    try:
        privacy_info = ethical_guard.get_privacy_notice()
        return privacy_info
    except Exception as e:
        logger.error(f"Error getting privacy info: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve privacy information: {str(e)}"
        )


# Chat History Endpoints
@app.post("/api/conversations")
async def create_conversation(user_id: str = "default"):
    """
    Create a new chat conversation.
    
    Returns the conversation ID that should be used in subsequent explain requests.
    """
    try:
        conv_id = chat_db.create_conversation(user_id=user_id, title="New Chat")
        logger.info(f"Created new conversation: {conv_id}")
        return {
            "conversation_id": conv_id,
            "title": "New Chat",
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create conversation: {str(e)}"
        )


@app.get("/api/conversations")
async def get_conversations(user_id: str = "default", limit: int = 50):
    """
    Get all conversations for a user.
    
    Returns a list of conversations ordered by most recent activity.
    """
    try:
        if limit < 1 or limit > 100:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 100")
        
        conversations = chat_db.get_user_conversations(user_id=user_id, limit=limit)
        return {
            "conversations": conversations,
            "count": len(conversations)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve conversations: {str(e)}"
        )


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """
    Get all messages in a specific conversation.
    
    Returns the conversation metadata and all messages ordered chronologically.
    """
    try:
        # Get conversation metadata
        conversation = chat_db.get_conversation_by_id(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get all messages in the conversation
        messages = chat_db.get_conversation_messages(conversation_id)
        
        return {
            "conversation": conversation,
            "messages": messages,
            "message_count": len(messages)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation {conversation_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve conversation: {str(e)}"
        )


@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Delete a conversation and all its messages.
    
    This action cannot be undone.
    """
    try:
        # Verify conversation exists
        conversation = chat_db.get_conversation_by_id(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        chat_db.delete_conversation(conversation_id)
        logger.info(f"Deleted conversation: {conversation_id}")
        
        return {
            "status": "deleted",
            "conversation_id": conversation_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation {conversation_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete conversation: {str(e)}"
        )


@app.put("/api/conversations/{conversation_id}/title")
async def update_conversation_title(conversation_id: str, title: str):
    """
    Update the title of a conversation.
    """
    try:
        # Verify conversation exists
        conversation = chat_db.get_conversation_by_id(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        if not title or len(title) > 100:
            raise HTTPException(status_code=400, detail="Title must be between 1 and 100 characters")
        
        chat_db.update_conversation_title(conversation_id, title)
        logger.info(f"Updated conversation title: {conversation_id} -> {title}")
        
        return {
            "status": "updated",
            "conversation_id": conversation_id,
            "title": title
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating conversation title {conversation_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update conversation title: {str(e)}"
        )


@app.get("/api/chat/stats")
async def get_chat_statistics():
    """
    Get chat history database statistics.
    
    Returns aggregate data about conversations and messages.
    """
    try:
        stats = chat_db.get_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error getting chat statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve chat statistics: {str(e)}"
        )


@app.post("/api/ethics/validate-code")
async def validate_code_safety(request: CodeExplanationRequest):
    """
    Validate code for safety, privacy, and quality.
    Phase 3: Code validation endpoint.
    """
    try:
        # Sanitize code
        sanitized_code, warnings = ethical_guard.sanitize_code(request.code)
        
        # Check for bias
        bias_check = ethical_guard.check_bias(request.code)
        
        # Quality analysis
        quality = ethical_guard.check_code_quality(request.code)
        
        return {
            "is_safe": len(warnings) == 0,
            "warnings": warnings,
            "bias_analysis": bias_check,
            "quality_metrics": quality,
            "sanitized_code": sanitized_code if len(warnings) > 0 else None
        }
    except Exception as e:
        logger.error(f"Error validating code: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to validate code: {str(e)}"
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting AI Code Explainer API (Phase 3: Enhanced)...")
    logger.info("Testing Groq API connection...")
    
    if test_groq_connection():
        logger.info("✓ Groq API connection successful")
    else:
        logger.warning("✗ Groq API connection failed - check your GROQ_API_KEY")
    
    # Initialize Phase 3 components
    logger.info("✓ Performance monitoring active")
    logger.info("✓ Ethical AI safeguards enabled")
    logger.info("✓ Chat history database initialized")
    
    # RAG system uses lazy loading (loads on first use)
    logger.info("✓ RAG system configured (lazy loading - will initialize on first use)")
    logger.info("\nPhase 3 Endpoints:")
    logger.info("  - Explanation: /api/explain, /api/explain-rag")
    logger.info("  - Chat History: /api/conversations, /api/chat/stats")
    logger.info("  - Metrics: /api/metrics/performance, /api/metrics/history")
    logger.info("  - Ethics: /api/ethics/privacy, /api/ethics/validate-code")
    logger.info("  - RAG: /api/rag/stats")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down AI Code Explainer API...")
    logger.info(f"Total requests processed: {performance_monitor.total_requests}")
