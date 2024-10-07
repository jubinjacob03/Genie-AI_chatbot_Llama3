import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Genie AI Chat",
    page_icon="🧞‍♂️",
    layout="centered"
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not set. Please set it in the .env file.")
else:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f4;
            color: #333;
            font-family: 'Roboto', sans-serif;
        }
        .main {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }
        h1 {
            color: #673ab7; 
            font-size: 3rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        .chat-container {
            width: 100%;
            max-width: 600px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            background-color: white;
            overflow: hidden;
            margin-bottom: 2rem;
        }
        .message {
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        .user {
            background-color: #ffbb33;
            color: #222;
            align-self: flex-end;
        }
        .assistant {
            background-color: #673ab7; 
            color: white;
            align-self: flex-start;
        }
        .stChatInput {
            margin-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🧞‍♂️ Genie AI")

with st.container():
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f'<div class="message user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message assistant">{message["content"]}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

user_prompt = st.chat_input("Ask Genie...")

if user_prompt:
    st.markdown(f'<div class="message user">{user_prompt}</div>', unsafe_allow_html=True)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": "You are a helpful assistant with a genie theme"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    st.markdown(f'<div class="message assistant">{assistant_response}</div>', unsafe_allow_html=True)
