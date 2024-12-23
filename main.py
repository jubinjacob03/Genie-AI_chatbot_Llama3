import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from address import get_current_ip, is_allowed_to_prompt
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

st.set_page_config(
    page_title="Genie AI Chat",
    page_icon="🪄",
    layout="centered"
)

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
        border-radius: 18px;
        background-color: #444;
        color: white;
        text-align: center;
        cursor: pointer;
        width: 100%;
        transition: background-color 0.2s ease-in-out;
    }
    .prompt-button:hover {
        background-color: #555;
    }
    .stTextInput > div {
            border-radius: 18px;}

    .stTextInput > div > div {
            border-radius: 18px;}
    .stTextInput > div > div > input {
        background-color: #333;
        color: white;
        padding: 10px;
        border: 1px solid #444;
        border-radius: 18px;
    }
    .stButton button {
        background-color: #444;
        color: white;
        border-radius: 18px;
        transition: background-color 0.2s ease-in-out;
    }
    .stButton button:hover {
        background-color: #555;
    }
    .response-container {
        position: relative;
        padding: 20px;
        background-color: #222;
        border-radius: 18px;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    #response_text {
        margin-bottom: 10px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ_API_KEY not set. Please set it in the .env file.")
else:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

try:
    client = Groq()
except Exception as e:
    logging.error(f"Failed to create Groq client: {e}")
    st.error("Unable to connect to the Groq service. Please try again later.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "prompt_input" not in st.session_state:
    st.session_state.prompt_input = ""

st.markdown('<div class="main-title">Genie AI 🪄</div>', unsafe_allow_html=True)
st.image("genie.png", width=120)

button_labels = [
    'Tell me an interesting fact',
    'Create a morning routine',
    'Quiz me on world capitals',
    'Tell me a fairy tale story'
]

cols = st.columns(len(button_labels))


def set_prompt(prompt):
    st.session_state.prompt_input = prompt


for col, label in zip(cols, button_labels):
    with col:
        st.button(label, on_click=lambda l=label: set_prompt(l))

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_prompt = st.text_input(" ", key="prompt_input",
                            placeholder=" Ask Genie...")

if user_prompt:
    current_ip = get_current_ip()

    if current_ip:
        if is_allowed_to_prompt(current_ip):
            st.session_state.chat_history.append(
                {"role": "user", "content": user_prompt}
            )

            messages = [
                {"role": "system",
                 "content": "You are a helpful assistant with a genie theme"},
                *st.session_state.chat_history
            ]

            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages
                )

                assistant_response = response.choices[0].message.content
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": assistant_response}
                )

                with st.chat_message("assistant"):
                    response_div = f"""
                    <div class="response-container">
                        <span id="response_text">{assistant_response}</span>
                    </div>
                    """
                    st.markdown(response_div, unsafe_allow_html=True)
            except Exception as e:
                logging.error(f"Error during API request: {e}")
                st.error(
                    "An error occurred while processing your request. Please try again.")
        else:
            st.error(
                "Free prompt limit reached. Please wait for the cooldown period (20 days) to reset.")
    else:
        st.error(
            "Could not retrieve your IP address. Please check your network connection.")
