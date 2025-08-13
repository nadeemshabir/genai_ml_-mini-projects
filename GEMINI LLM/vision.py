import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
import pathlib
import textwrap
from PIL import Image
# Load the API key
load_dotenv()
import io

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,image):
    model = genai.GenerativeModel('models/gemini-2.5-pro')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(io.BytesIO(uploaded_file.read()))
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the image")

## If ask button is clicked

if submit:
    
    response=get_gemini_response(input,image)
    st.subheader("The Response is")
    st.write(response)



# import google.generativeai as genai

# genai.configure(api_key="AIzaSyAR8I0fhRSEjrlxhwLrwt7KC3wQGLqpui8")

# for model in genai.list_models():
#     print(model.name, "->", model.supported_generation_methods)
