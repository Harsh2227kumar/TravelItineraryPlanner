"""
Pydantic schemas for the FastAPI backend.
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    query: str
    channel: str = "web"

class Suggestion(BaseModel):
    question: str
    answer: str

class ChatResponse(BaseModel):
    type: str # 'answer', 'fallback_soft', 'fallback_hard'
    answer: Optional[str] = None
    score: Optional[float] = None
    clarification: Optional[str] = None
    suggestions: Optional[List[Suggestion]] = None
    message: Optional[str] = None

class FeedbackRequest(BaseModel):
    query: str
    intent: str
    confidence: float
    answer: str
    was_fallback: bool
