import time
import json
import board
import adafruit_dht
import paho.mqtt.client as mqtt
from gpiozero import InputDevice, MotionSensor

# === MQTT Setup ===
BROKER = "localhost"  # or backend's IP if running elsewhere
PORT = 1883
TOPIC = "skyranger/sensor/all"
client = mqtt.Client(client_id="sensor_publisher", callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
client.connect(BROKER, PORT, 60)
client.loop_start()

# === Sensor Setup ===
DHT_SENSOR = adafruit_dht.DHT11(board.D4)
VIBRATION_PIN = 17
PIR_PIN = 27

vibration_sensor = InputDevice(VIBRATION_PIN)
pir_sensor = MotionSensor(PIR_PIN)

print("📡 SkyRanger Sensor System Active...")
print("Press Ctrl+C to stop\n")

try:
    while True:
        try:
            temp = DHT_SENSOR.temperature
            hum = DHT_SENSOR.humidity
        except RuntimeError:
            temp, hum = None, None

        motion = pir_sensor.motion_detected
        vibration = vibration_sensor.is_active

        payload = {
            "dht11": {"temperature": temp, "humidity": hum},
            "pir": {"motion": int(motion)},
            "vibration": {"vibration": int(vibration)}
        }

        # Publish to MQTT
        client.publish(TOPIC, json.dumps(payload))
        print(f"🌡️ Temp: {temp}°C | 💧 Hum: {hum}% | 🧍 Motion: {motion} | ⚡ Vibration: {vibration}")
        print("📤 Published:", payload)
        print("-" * 50)

        time.sleep(2)

except KeyboardInterrupt:
    print("\nExiting sensor monitor...")
    client.loop_stop()
    client.disconnect()
