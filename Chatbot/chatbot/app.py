from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import os
from dotenv import load_dotenv

os.environ["OPENAI_API_KEY"]= os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]= os.getenv("LANGCHAIN_API_KEY")

#prompt template
prompt= ChatPromptTemplate.messages(
    [
        ("system","you are a helpful assisstant please reponse to the queries"),
        ("user", "Question:{question}")
    ]
)

#streamlit framework
st.title("Langchain Demo with OPENAI")
input_text= st.text_input("search the topic u want")

#openai LLm
llm = ChatOpenAI(model= "gpt-3.5-turbo")
output_parser= StrOutputParser()
chain= prompt|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))

