from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from langchain.chains import LLMChain
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Load OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(openai_api_key=api_key, temperature=0.8)

class Commaseparatedoutput(BaseOutputParser):
    def parse(self, text: str):
        return text.strip().split(",")
    
# Streamlit page configuration
st.set_page_config(page_title="Synonyms Generator🤖")
st.header("🤖 Synonyms Generator 🤖")

template = "Yoiu are a helpful assistant. When the user provides any input, you should generate 5 words synonyms in a comma-separated list."
human_template = "{text}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system",template),
    ("human",human_template)
])

llm_chain = LLMChain(llm = chat, prompt = chat_prompt, output_parser = Commaseparatedoutput())
input_text = st.text_input("Enter a word or phrase:", " ")

if st.button("Generate Synonyms"):
    if input_text:
        response = llm_chain.predict(text = input_text)
        st.write("Synonyms: "," , ".join(response))
    else:
        st.write("Please Enter a word or phrase.")
