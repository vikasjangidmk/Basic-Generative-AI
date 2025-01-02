import streamlit as st
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(page_title="My ChatBot🤖")
st.header("🤖 OpenAI ChatBot")

# Load OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model
model = ChatOpenAI(openai_api_key=api_key, temperature=0.8)

# Initialize session state for storing chat messages
if 'mymessages' not in st.session_state:
    st.session_state['mymessages'] = [
        SystemMessage(content="You are a Gen AI ChatBot 🤖 and your work is to answer my questions.")
    ]

# Function to get chat model response
def chatmodel_response(question):
    # Add user's question to the messages
    st.session_state['mymessages'].append(HumanMessage(content=question))
    
    # Generate response using the model
    response = model(st.session_state['mymessages'])
    
    # Add AI's response to the messages
    st.session_state['mymessages'].append(AIMessage(content=response.content))
    
    return response.content

# User input section
input_question = st.text_input("Input:", key="Input")
submit_button = st.button("Ask Question")

if submit_button and input_question.strip():
    # Generate and display response
    response = chatmodel_response(input_question)
    st.subheader("This is your Response -> ")
    st.write(response)
