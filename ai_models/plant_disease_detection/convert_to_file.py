import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model("plant_disease_model.keras")

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.target_spec.supported_ops = [
    tf.lite.OpsSet.TFLITE_BUILTINS
]
converter._experimental_lower_tensor_list_ops = True
converter.target_spec.supported_types = [tf.float32]
tflite_model = converter.convert()

with open("plant_disease_model_v214.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ Model converted for TF 2.14 runtime compatibility")
