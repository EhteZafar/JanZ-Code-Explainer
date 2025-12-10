"""
FastAPI Backend for AI Code Explainer
Provides REST API endpoint for code explanation using LLaMA 3.3 70B via Groq
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging

from groq_integration import get_code_explanation, test_groq_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Explainer API",
    description="API for explaining code using LLaMA 3.3 70B Versatile",
    version="1.0.0"
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
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "explain": "/api/explain (POST)",
            "health": "/health (GET)",
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
    Explain code using LLaMA 3.3 70B Versatile.
    
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


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting AI Code Explainer API...")
    logger.info("Testing Groq API connection...")
    
    if test_groq_connection():
        logger.info("✓ Groq API connection successful")
    else:
        logger.warning("✗ Groq API connection failed - check your GROQ_API_KEY")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down AI Code Explainer API...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
