from fastapi import FastAPI
from routes import telemetry

app = FastAPI(title="SkyRanger Backend")

app.include_router(telemetry.router, prefix="/api/telemetry")

@app.get("/")
def root():
    return {"message": "SkyRanger backend running"}

