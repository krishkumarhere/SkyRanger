from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.mqtt_service import start_mqtt_client # Import MQTT background service
from app.routes import telemetry #import more routers (telemetry, ai, sensors, etc.)

app = FastAPI(title="SkyRanger Backend", version="1.0")

# --- CORS setup  ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # replace with your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup event: launch background MQTT listener ---
@app.on_event("startup")
def startup_event():
    print("[INIT] Starting MQTT client...")
    start_mqtt_client()
    print("[INIT] MQTT service running")

app.include_router(telemetry.router)


@app.get("/")
def root():
    return {"status": "ok", "message": "SkyRanger backend running"}

# --- Uncomment when telemetry route is ready ---
# app.include_router(telemetry.router)

# --- Run only if executed directly (not when imported) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
