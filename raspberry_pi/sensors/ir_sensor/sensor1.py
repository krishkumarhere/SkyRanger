import RPi.GPIO as GPIO
import time
import json
import os

# --- Load config.json ---
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

sensor_cfg = config["ir_sensor"]["sensor1"]
IR_PIN = sensor_cfg["pin"]
DELAY = sensor_cfg["delay"]

# --- GPIO setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print(f"Starting IR sensor test on GPIO {IR_PIN}. Press Ctrl+C to exit.")

try:
    while True:
        state = GPIO.input(IR_PIN)
        if state == 0:
            print("Obstacle detected!")
        else:
            print("No obstacle")
        time.sleep(DELAY)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
