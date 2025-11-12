import time
import board
import adafruit_dht
from gpiozero import InputDevice, MotionSensor

# === Sensor Setup ===
DHT_SENSOR = adafruit_dht.DHT11(board.D4)  # DHT11 on GPIO4
VIBRATION_PIN = 17
PIR_PIN = 27

vibration_sensor = InputDevice(VIBRATION_PIN)
pir_sensor = MotionSensor(PIR_PIN)

print("📡 SkyRanger Sensor System Active...")
print("Press Ctrl+C to stop\n")

try:
    while True:
        try:
            temp = DHT_SENSOR.temperature  #Temperature
            hum = DHT_SENSOR.humidity
        except RuntimeError:
            temp, hum = None, None

        motion = pir_sensor.motion_detected #Motion
        vibration = vibration_sensor.is_active #Vibration

        print(f"🌡️ Temp: {temp}°C | 💧 Hum: {hum}% | 🧍 Motion: {motion} | ⚡ Vibration: {vibration}")

        if motion:
            print("🚨 Motion detected!")
        if vibration:
            print("⚠️ Vibration detected!")

        time.sleep(2)

except KeyboardInterrupt:
    print("\nExiting sensor monitor...")

