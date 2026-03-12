"""
FastAPI application entry point.
"""
from fastapi import FastAPI, HTTPException
import sys
import os

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.api.schemas import ChatRequest, ChatResponse
from src.core import get_answer, get_top_n_answers
from src.core.preprocessor import preprocess
from src.core.intent import predict_intent
from src.core.entities import extract_entities
from src.core.fallback import handle_response
from src.core.analytics import log_interaction, get_analytics_summary, get_logs_df

app = FastAPI(title="College FAQ Chatbot API", version="1.0.0")

@app.get("/health")
def health_check():
    """Health check endpoint to ensure the API is running."""
    return {"status": "ok", "message": "College FAQ Chatbot API is running"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    """
    Process a user query and return the appropriate response (answer or fallback).
    """
    try:
        user_input = request.query
        processed_input = preprocess(user_input)
        
        # Core ML logic
        intent = predict_intent(processed_input)
        entities = extract_entities(user_input)
        answer, score, answer_intent, answer_entities = get_answer(user_input)
        
        # Decide response type (answer, soft fallback, hard fallback)
        response = handle_response(
            query=user_input,
            answer=answer,
            score=score,
            get_top_n_fn=get_top_n_answers
        )
        
        # Ensure we log the interaction
        was_fallback = response["type"] in ["fallback_soft", "fallback_hard"]
        # Save exact string answer or use default empty string
        logged_answer = response.get("answer", "")
        if response["type"] == "fallback_hard":
            logged_answer = response.get("message", "")
        
        log_interaction(
            query=user_input,
            intent=intent,
            confidence=score,
            answer=logged_answer,
            was_fallback=was_fallback
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/summary")
def analytics_summary():
    """
    Get high-level analytics for the dashboard.
    """
    try:
        summary = get_analytics_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/logs")
def analytics_logs():
    """
    Get raw logs for the dashboard table.
    """
    try:
        df = get_logs_df()
        # Remove timestamp to avoid datetime serialization issues
        # Or convert to string
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = df['timestamp'].astype(str)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/unhandled")
def analytics_unhandled():
    """
    Get top unhandled queries for the dashboard.
    """
    try:
        df = get_logs_df()
        if df.empty:
            return []
        fallbacks = df[df["was_fallback"] == 1]
        top_unhandled = fallbacks["query"].value_counts().head(10).to_dict()
        return [{"query": q, "count": c} for q, c in top_unhandled.items()]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
