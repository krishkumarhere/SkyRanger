import json
import threading
import paho.mqtt.client as mqtt

BROKER_IP = "localhost"  # or your Pi's IP if backend runs elsewhere
PORT = 1883
TOPIC = "skyranger/telemetry"

latest_data = {}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[MQTT] Connected to broker.")
        client.subscribe(TOPIC)
        print(f"[MQTT] Subscribed to topic: {TOPIC}")
    else:
        print(f"[MQTT] Connection failed with code {rc}")

def on_message(client, userdata, msg):
    global latest_data
    try:
        payload = msg.payload.decode()          
        data = json.loads(payload)
        latest_data = data
        print(f"[MQTT] Received telemetry: {data}")
    except Exception as e:
        print(f"[MQTT] Message handling error: {e}")

def get_latest_data():
    """Return the most recent telemetry."""
    return latest_data if latest_data else {"status": "no data yet"}

def start_mqtt_client():
    """Run MQTT listener in a background thread."""
    client = mqtt.Client(client_id="FastAPI_Backend")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_IP, PORT, 60)

    thread = threading.Thread(target=client.loop_forever)
    thread.daemon = True
    thread.start()

    print("[MQTT] Client started in background thread.")
