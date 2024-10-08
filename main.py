import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Genie AI Chat",
    page_icon="🪄",
    layout="centered"
)

# Load the Poppins font and dark background
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    * {
        font-family: 'Poppins', sans-serif;
        color: white;
    }
    body {
        background-color: #1b1b1d;
    }
    .main-title {
        text-align: center;
        font-size: 3em;
        margin-top: 20px;
    }
    .prompt-buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 30px;
    }
    .prompt-button {
        padding: 15px 20px;
        border-radius: 5px;
        background-color: #444;
        color: white;
        text-align: center;
        cursor: pointer;
    }
    .stTextInput > div > div > input {
        background-color: #333;
        color: white;
        border-radius: 20px;
    }
    .stButton button {
        background-color: #444;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not set. Please set it in the .env file.")
else:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Chat history session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title and Image
st.markdown('<div class="main-title">Genie AI 🪄</div>', unsafe_allow_html=True)
st.image("genie.png", width=120)

# Quick Start Prompts
st.markdown("""
    <div class="prompt-buttons">
        <div class="prompt-button" onclick="document.getElementById('prompt_input').value='Make up a story';">Make up a story</div>
        <div class="prompt-button" onclick="document.getElementById('prompt_input').value='Create a morning routine';">Create a morning routine</div>
        <div class="prompt-button" onclick="document.getElementById('prompt_input').value='Quiz me on world capitals';">Quiz me on world capitals</div>
        <div class="prompt-button" onclick="document.getElementById('prompt_input').value='Plan a mental health day';">Plan a mental health day</div>
    </div>
""", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
user_prompt = st.text_input("Ask Genie...", key="prompt_input")

# Handle user input
if user_prompt:
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

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
