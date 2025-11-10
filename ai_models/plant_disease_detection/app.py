import streamlit as st
import numpy as np
from PIL import Image

# ✅ Dual import: works both on Pi and laptop
try:
    import tflite_runtime.interpreter as tflite
    Interpreter = tflite.Interpreter
    BACKEND = "TFLite Runtime"
except ModuleNotFoundError:
    from tensorflow.lite.python.interpreter import Interpreter
    BACKEND = "TensorFlow Lite (TF)"

MODEL_PATH = "plant_disease_model.tflite"
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

st.sidebar.markdown(f"**Backend:** {BACKEND}")


# Class names (same as training)
CLASS_NAMES = [
    'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
    'PlantVillage', 'Potato___Early_blight', 'Potato___healthy',
    'Potato___Late_blight', 'Tomato_Bacterial_spot', 'Tomato_Early_blight',
    'Tomato_healthy', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
    'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
    'Tomato__Target_Spot', 'Tomato__Tomato_mosaic_virus',
    'Tomato__Tomato_YellowLeaf__Curl_Virus'
]
HEALTHY_CLASSES = ['Pepper__bell___healthy', 'Potato___healthy', 'Tomato_healthy']

st.title("🌿 Plant Disease Detection (TFLite)")
st.write("Upload a leaf image for prediction")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Leaf", use_column_width=True)

    # Preprocess
    img = image.resize((128, 128))
    img_array = np.expand_dims(np.asarray(img, dtype=np.float32) / 255.0, axis=0)

    # Inference
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])[0]

    pred_idx = np.argmax(output_data)
    confidence = float(np.max(output_data)) * 100
    predicted_class = CLASS_NAMES[pred_idx]

    color = "green" if predicted_class in HEALTHY_CLASSES else "red"
    st.markdown(
        f"<h2 style='color:{color}'>Prediction: {predicted_class}</h2>",
        unsafe_allow_html=True
    )
    st.write(f"Confidence: {confidence:.2f}%")
