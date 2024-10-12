import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Genie AI Chat",
    page_icon="🪄",
    layout="centered"
)

# Load custom CSS for styling
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
    .prompt-button {
        padding: 15px 20px;
        border-radius: 5px;
        background-color: #444;
        color: white;
        text-align: center;
        cursor: pointer;
        width: 100%;  /* Make buttons fill their column */
    }
    .stTextInput > div > div > input {
        background-color: #333;
        color: white;
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

# Retrieve API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not set. Please set it in the .env file.")
else:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# Initialize chat history in session state if not present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

# Title and Image
st.markdown('<div class="main-title">Genie AI 🪄</div>', unsafe_allow_html=True)
st.image("genie.png", width=120)

# Quick Start Prompts using columns for horizontal layout
button_labels = [
    'Tell me an interesting fact',
    'Create a morning routine',
    'Quiz me on world capitals',
    'Tell me a fairy tale story'
]

# Create as many columns as there are buttons
cols = st.columns(len(button_labels))

# Define a function to set the prompt input when a button is clicked
def set_prompt(prompt):
    st.session_state.prompt_input = prompt

for col, label in zip(cols, button_labels):
    with col:
        st.button(label, on_click=lambda l=label: set_prompt(l))

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
user_prompt = st.text_input(" ", key="prompt_input", placeholder=" Ask Genie...")

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
                Copy
            </button>
            <script>
                function copyToClipboard() {{
                    const responseText = document.getElementById('response_text').innerText;
                    navigator.clipboard.writeText(responseText);
                }}
            </script>
            </div>
            """

        st.markdown(response_div, unsafe_allow_html=True)
