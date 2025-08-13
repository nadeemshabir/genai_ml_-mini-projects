import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
# Langchain's FAISS vector store is now in the 'langchain_community' package
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI model
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY not found. Please set it in your .env file.")
else:
    genai.configure(api_key=api_key)


def get_pdf_text(pdf_docs):
    """Extracts text from a list of uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
    return text


def get_text_chunks(text):
    """Splits the text into smaller chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    """Creates and saves a FAISS vector store from text chunks."""
    # Use the newer and more capable text embedding model
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    try:
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        # Save the vector store locally
        vector_store.save_local("faiss_index")
    except Exception as e:
        st.error(f"Error creating vector store: {e}")


def get_conversational_chain():
    """Creates a question-answering chain with a specific prompt."""
    prompt_template = """
    Answer the question as detailed as possible from the provided context. Make sure to provide all the details.
    If the answer is not in the provided context, just say, "The answer is not available in the context."
    Do not provide a wrong answer.\n\n
    Context:\n{context}\n
    Question:\n{question}\n

    Answer:
    """
    # Use the newer, faster, and more capable Gemini model
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain


def user_input(user_question):
    """Handles user input, performs similarity search, and displays the answer."""
    # Use the same embedding model as when you created the store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    
    try:
        # Load the local FAISS index
        # IMPORTANT: allow_dangerous_deserialization is required for loading local FAISS indexes
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)

        chain = get_conversational_chain()
        
        response = chain(
            {"input_documents": docs, "question": user_question},
            return_only_outputs=True
        )

        print(response) # For debugging in the terminal
        st.write("Reply: ", response["output_text"])

    except FileNotFoundError:
        st.warning("FAISS index not found. Please upload and process PDF files first.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Chat with PDFs", page_icon="💁")
    st.header("Chat with Multiple PDFs using Gemini Pro 💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click 'Process'", accept_multiple_files=True)
        
        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if raw_text:
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        st.success("Done! You can now ask questions.")
                    else:
                        st.warning("Could not extract text from the PDF(s).")
            else:
                st.warning("Please upload at least one PDF file.")


if __name__ == "__main__":
    main()