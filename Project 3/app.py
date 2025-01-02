import streamlit as st
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
import streamlit as st
from dotenv import load_dotenv
# Load environment variables
import os 
load_dotenv()
api_key = os.getenv("OPEN_API_KEY")

from langchain.llms import OpenAI
# Set up Streamlit UI
st.set_page_config(page_title="Document Search Chatbot")
st.header(" 🔍 Document Search Chatbot 👋👋  I am your chatbot 💬 , Ask me a question ❓  🤖")

loader = TextLoader('mytext.txt')
docs = loader.load()


# Calculate some statistics
num_total_characters = sum([len(x.page_content) for x in docs])
st.write(f"Now you have {len(docs)} documents that have an average of {num_total_characters / len(docs):,.0f} characters (smaller pieces)")

# Get embeddings ready
embeddings = OpenAIEmbeddings(openai_api_key=api_key )
docsearch = FAISS.from_documents(docs, embeddings)
model= OpenAI(openai_api_key=api_key, temperature=0.9)

qa = RetrievalQA.from_chain_type(llm=model, chain_type="stuff", retriever=docsearch.as_retriever())

# Text input for user query
user_query = st.text_input("Ask me a question:", "")

# Button to trigger the search
if st.button("Search"):
    # Perform the question-answering
    if user_query:
        response = qa.run(user_query)
        # Display the answer
        st.write("Answer:", response)
    else:
        st.write("Please ask a question.")
