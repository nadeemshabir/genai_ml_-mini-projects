import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load the API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key loaded
if not api_key:
    st.error("❌ GOOGLE_API_KEY not found in environment variables.")
    st.stop()

genai.configure(api_key=api_key)

# Set up model
try:
    model = genai.GenerativeModel("models/gemini-2.5-flash-lite-preview-06-17")
except Exception as e:
    st.error(f"❌ Error initializing model: {e}")
    st.stop()

# Function to get response
def get_gemini_response(question):
    try:
        response = model.generate_content(question)
        text = getattr(response, 'text', None)
        if text and text.strip():
            return text.strip()
        else:
            return "⚠️ Gemini returned an empty response."
    except Exception as e:
        return f"❌ Error from Gemini: {e}"

# Streamlit UI
st.set_page_config(page_title="Gemini Chat", layout="centered")
st.title("💬 Gemini LLM Chat")

user_input = st.text_input("Ask Gemini something:", key="user_input")

if st.button("Get Response"):
    if not user_input.strip():
        st.warning("⚠️ Please enter a valid question.")
    else:
        with st.spinner("🧠 Thinking..."):
            answer = get_gemini_response(user_input)
        st.subheader("🧠 Gemini Response")
        st.write(answer)
