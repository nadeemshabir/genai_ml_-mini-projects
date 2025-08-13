from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

from PIL import Image
import streamlit as st
# Set the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to generate text using Google Generative AI
model= genai.GenerativeModel("gemini-1.5-flash")
def get_gemini_response(image_parts,prompt):
    response = model.generate_content([prompt]+ image_parts,)
    return response.text
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts=[
            {
                "data": bytes_data,
                "mime_type": uploaded_file.type}
        ]
        return image_parts
    else:
        raise ValueError("No file uploaded")
       

# Streamlit app configuration
st.set_page_config(page_title="Invoice Extractor", page_icon=":money_with_wings:", layout="wide")
st.title("Invoice Extractor")
user_prompt = st.text_input("Enter your prompt here:")
uploaded_file = st.file_uploader("Upload an invoice image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Invoice", use_column_width=True)

if st.button("Submit") and uploaded_file:
    image_parts = input_image_setup(uploaded_file)
    final_prompt = user_prompt if user_prompt else "Extract all invoice details in structured format."
    response = get_gemini_response(image_parts, final_prompt)
    st.text_area("Response from Gemini AI:", value=response, height=300)