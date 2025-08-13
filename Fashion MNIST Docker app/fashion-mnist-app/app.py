import streamlit as st
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# Load your model
model = load_model('trained_fashion_mnist_model.h5', compile=False)


# Class labels for Fashion MNIST
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# App title
st.title("👗 Fashion MNIST Image Classifier")

# Upload image
uploaded_file = st.file_uploader("Upload a 28x28 grayscale image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert('L')  # Convert to grayscale
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Resize and preprocess
    image = image.resize((28, 28))
    image_array = np.array(image) / 255.0
    image_array = image_array.reshape(1, 28, 28, 1)

    # Predict
    prediction = model.predict(image_array)
    predicted_label = class_names[np.argmax(prediction)]

    st.subheader("Prediction:")
    st.write(f"🧠 This looks like a **{predicted_label}**")
