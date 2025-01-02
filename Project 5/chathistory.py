

from dotenv import load_dotenv
load_dotenv() 
import streamlit as st
import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question, history):
    # Concatenate the chat history to provide context
    context = ""
    for user_role, user_text, bot_role, bot_text in history:
        context += f"{user_role}: {user_text}\n{bot_role}: {bot_text}\n"
    # Append the current question to the context
    context += f"You: {question}\nBot:"
    # Get the response from the model
    response = chat.send_message(context, stream=True)
    response_text = ''.join(chunk.text for chunk in response)
    return response_text

# Function to load chat history from a file
def load_chat_history(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

# Function to save chat history to a file
def save_chat_history(file_path, chat_history):
    with open(file_path, 'w') as file:
        json.dump(chat_history, file)

# File path to store chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Load chat history if it exists
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = load_chat_history(CHAT_HISTORY_FILE)

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Your Chatbot 🫂")

# User input
input = st.text_input("Input your question: ", key="input")
submit = st.button("Ask the question")

# Handle user input
if submit and input:
    response = get_gemini_response(input, st.session_state['chat_history'])
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input, "Bot", response))
    # Save chat history to file
    save_chat_history(CHAT_HISTORY_FILE, st.session_state['chat_history'])

# Display chat history
st.subheader("Your chatbot")

for user_role, user_text, bot_role, bot_text in st.session_state['chat_history']:
    with st.container():
        st.markdown(f"""
            <div style="padding: 10px; border-radius: 10px; background-color: #f0f0f5; margin-bottom: 10px; color: #000;">
                <strong>{user_role}</strong>: {user_text}
            </div>
            <div style="padding: 10px; border-radius: 10px; background-color: #e0f7fa; margin-bottom: 10px; color: #000;">
                <strong>{bot_role}</strong>: {bot_text}
            </div>
            """, unsafe_allow_html=True)



