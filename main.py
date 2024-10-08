import os
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
    .response-container {
        position: relative;
        padding: 20px;
        background-color: #222;
        border-radius: 5px;
        margin-top: 10px;
    }
    .copy-button {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: #FFC107;
        color: black;
        border: none;
        border-radius: 5px;
        padding: 5px 10px;
        cursor: pointer;
        font-size: 0.9em;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .copy-button:hover {
        background-color: #FFB300;
    }
    #response_text {
        margin-bottom: 10px;
        margin-top: 40px;
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
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt})

    messages = [
        {"role": "system", "content": "You are a helpful assistant with a genie theme"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response})

    # After appending the assistant response to chat history
    with st.chat_message("assistant"):
        response_div = f"""
        <div class="response-container">
            <span id="response_text">{assistant_response}</span>
            <button class="copy-button" onclick="copyToClipboard()">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path>
                </svg>
                Copy
            </button>
        </div>
        <script>
            function copyToClipboard() {{
                const responseText = document.getElementById('response_text').innerText;
                navigator.clipboard.writeText(responseText);
            }}
        </script>
        """
        st.markdown(response_div, unsafe_allow_html=True)
