import streamlit as st
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from requests import get
from bs4 import BeautifulSoup

# Initialize the Ollama model (no API key required)
llama_model = Ollama(model="gemma2:2b")

# Define a prompt template for the chatbot (ChatGPT-like prompt)
prompt = PromptTemplate(
    input_variables=["history", "query", "product_data"],
    template="You are a helpful assistant. Here is the conversation history:\n{history}\n\n"
              "The user asked: {query}\n\n"
              "Based on this, and the following product data, provide a helpful response:\n{product_data}"
)

# Create an LLMChain
llm_chain = LLMChain(llm=llama_model, prompt=prompt)

# Streamlit chat interface
st.set_page_config(page_title="Flipkart Product ChatBot")
st.header("🤖 Flipkart Product ChatBot")

# Initialize memory (conversation history) in session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        SystemMessage(content="You are a helpful assistant that provides product details from Flipkart based on user queries.")
    ]

# Function to fetch Flipkart products based on a query
def fetch_flipkart_products(query):
    url = f"https://www.flipkart.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    products = []
    for item in soup.find_all("div", {"class": "_1AtVbE"}):
        title = item.find("a", {"class": "IRpwTa"})
        price = item.find("div", {"class": "_30jeq3"})

        if title and price:
            product_title = title.get_text()
            product_price = price.get_text()
            products.append({"title": product_title, "price": product_price})
    
    return products

# Function to generate chatbot responses based on history and user query
def chatbot_response(query):
    # Fetch product data based on the user query
    product_data = fetch_flipkart_products(query)
    
    # Format product data for the prompt
    formatted_product_data = "\n".join([f"Product: {p['title']} - Price: {p['price']}" for p in product_data])
    
    # Build history string for context
    history = ""
    for msg in st.session_state['messages']:
        if isinstance(msg, HumanMessage):
            history += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            history += f"Bot: {msg.content}\n"
    
    # Generate chatbot response using the LLMChain
    response = llm_chain.run(history=history, query=query, product_data=formatted_product_data)
    
    return response

# Streamlit UI: Display chat and input box
input_text = st.text_input("Ask me about Flipkart products:", key="input")

if input_text:
    # Display the user's message
    st.session_state['messages'].append(HumanMessage(content=input_text))
    
    # Get the chatbot's response
    response = chatbot_response(input_text)
    
    # Display the bot's response
    st.session_state['messages'].append(AIMessage(content=response))
    
    # Display the entire conversation (history + current exchange)
    for message in st.session_state['messages']:
        if isinstance(message, HumanMessage):
            st.write(f"**You:** {message.content}")
        elif isinstance(message, AIMessage):
            st.write(f"**Bot:** {message.content}")
