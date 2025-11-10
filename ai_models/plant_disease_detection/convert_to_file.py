import tensorflow as tf
from tensorflow import keras
import os

# Disable TF warnings about GPU and performance
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

print("🔹 Loading trained model...")
model = keras.models.load_model("plant_disease_model.keras")

print("🔹 Converting model to TensorFlow Lite format...")
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Optional optimizations (make model smaller & faster on Pi)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# Convert the model
tflite_model = converter.convert()

# Save the converted model
tflite_path = "plant_disease_model.tflite"
with open(tflite_path, "wb") as f:
    f.write(tflite_model)

print(f"✅ Conversion complete! File saved as {tflite_path}")
