import streamlit as st
import requests

from src.config import APP_TITLE, APP_DESCRIPTION
from src.ui.sidebar import render_sidebar
from src.ui.components import render_answer, render_fallback_ui

import os

# FastAPI Backend Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Configure page
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🎓",
    layout="wide"
)

# Render standard sidebar
render_sidebar()

# Main UI Header
st.title("🎓 College FAQ Chatbot")
st.markdown(APP_DESCRIPTION)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display standard chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask a question (e.g., 'What is the hostel fee?'):"):
    
    # 1. Add user message to UI state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Add empty assistant message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Call the FastAPI backend
                response = requests.post(
                    f"{API_URL}/chat", 
                    json={"query": prompt, "channel": "web"},
                    timeout=5
                )
                response.raise_for_status()
                data = response.json()
                
                # Format based on response type (Answer vs Fallback)
                if data["type"] == "answer":
                    render_answer(data["answer"], data.get("score", 0))
                    # Add to text history
                    st.session_state.messages.append({"role": "assistant", "content": data["answer"]})
                    
                elif data["type"] == "fallback_soft":
                    render_fallback_ui(
                        data.get("clarification", "I'm not exactly sure. Did you mean:"),
                        data.get("suggestions", []),
                        show_advisor=True
                    )
                    hist_text = "I wasn't sure. Suggested related FAQs instead."
                    st.session_state.messages.append({"role": "assistant", "content": hist_text})
                    
                elif data["type"] == "fallback_hard":
                    render_fallback_ui(
                        data.get("message", "I don't have information on that."),
                        [],
                        show_advisor=True
                    )
                    st.session_state.messages.append({"role": "assistant", "content": "I couldn't answer that. Advisor contact provided."})
                    
            except requests.exceptions.ConnectionError:
                err = "⚠️ Cannot connect to the backend server. Is FastAPI running on port 8000?"
                st.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
            except Exception as e:
                err = f"An error occurred: {e}"
                st.error(err)
                st.session_state.messages.append({"role": "assistant", "content": err})
