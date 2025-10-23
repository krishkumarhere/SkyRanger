import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load the trained model
model = load_model("plant_disease_model.keras")

# List of class names (16 classes)
class_names = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'PlantVillage', 'Potato___Early_blight', 'Potato___healthy',
    'Potato___Late_blight', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
    'Tomato_healthy', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot', 'Tomato__Tomato_mosaic_virus',
    'Tomato__Tomato_YellowLeaf__Curl_Virus'
]

# Define which classes are healthy
healthy_classes = ['Pepper__bell___healthy', 'Potato___healthy', 'Tomato_healthy']

st.title("🌿 Plant Disease Detection")
st.write("Upload a leaf image and see the disease prediction.")

# Upload file
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open and show image
    img = Image.open(uploaded_file)
    st.image(img, caption='Uploaded Leaf Image', use_column_width=True)
    
    # Preprocess the image
    img = img.resize((128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    # Make prediction
    pred = model.predict(img_array)
    pred_class = np.argmax(pred, axis=1)
    predicted_class_name = class_names[pred_class[0]]
    confidence = np.max(pred) * 100
    
    # Set color based on healthy or diseased
    if predicted_class_name in healthy_classes:
        color = 'green'
    else:
        color = 'red'
    
    st.markdown(f"<h2 style='color:{color}'>Predicted Disease: {predicted_class_name}</h2>", unsafe_allow_html=True)
    st.write(f"Confidence: {confidence:.2f}%")
