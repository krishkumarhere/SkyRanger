# app/services/mqtt_service.py
from datetime import datetime

latest_data = {
    "temperature": None,
    "humidity": None,
    "motion": None,
    "vibration": None,
    "timestamp": None
}

def update_sensor_data(payload: dict):
    """Called whenever MQTT message arrives"""
    try:
        dht = payload.get("dht11", {})
        pir = payload.get("pir", {})
        vib = payload.get("vibration", {})

        latest_data["temperature"] = dht.get("temperature")
        latest_data["humidity"] = dht.get("humidity")
        latest_data["motion"] = pir.get("motion")
        latest_data["vibration"] = vib.get("vibration")
        latest_data["timestamp"] = datetime.now().isoformat()

        print("[MQTT_SERVICE] Updated:", latest_data)

    except Exception as e:
        print(f"[MQTT_SERVICE] Failed to update data: {e}")


def get_latest_sensor_data():
    return latest_data
