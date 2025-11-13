from fastapi import FastAPI
from app.core.mqtt_client import start_mqtt
from app.services import mqtt_service

app = FastAPI(title="SkyRanger Backend (MQTT Enabled)")

# Start MQTT on launch
start_mqtt()

@app.get("/")
def root():
    return {"message": "Backend running with MQTT 🚀"}

@app.get("/api/sensor/latest")
def get_latest_sensor():
    """Return latest data stored by MQTT service"""
    return mqtt_service.get_latest_sensor_data()
