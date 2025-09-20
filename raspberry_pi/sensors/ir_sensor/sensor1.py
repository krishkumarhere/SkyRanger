#!/usr/bin/env python3
"""
sensor1.py - Minimal IR sensor reader (IR1)
Works on laptop (mock GPIO) and Raspberry Pi
"""

import os
import json
import time
import logging
import signal
import sys

# --- GPIO import with mock fallback for laptop ---
try:
    import RPi.GPIO as GPIO
except ImportError:
    class MockGPIO:
        BCM = 'BCM'
        IN = 'IN'
        PUD_DOWN = 'PUD_DOWN'
        PUD_UP = 'PUD_UP'
        BOTH = 'BOTH'
        def setmode(self, mode): pass
        def setup(self, pin, mode, pull_up_down=None): pass
        def input(self, pin): return 1
        def add_event_detect(self, pin, edge, callback=None, bouncetime=0): pass
        def cleanup(self): pass
    GPIO = MockGPIO()
    print("Running with MockGPIO (no hardware)")

# --- load config ---
BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'config.json'))

try:
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
except Exception as e:
    print(f"ERROR reading config.json: {e}")
    sys.exit(1)

# --- read sensor parameters ---
IR_PIN = int(config.get('IR1_GPIO', 17))
DEBOUNCE_SEC = float(config.get('IR_DEBOUNCE', 0.15))
PULL = str(config.get('IR_PULL', 'down')).lower()
ACTIVE_LOW = bool(config.get('IR_ACTIVE_LOW', True))

PUD = GPIO.PUD_UP if PULL == 'up' else GPIO.PUD_DOWN

# --- logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ir_sensor1')

_last_event = 0.0  # timestamp for software debounce

# --- cleanup function ---
def cleanup():
    logger.info("Cleaning up GPIO")
    try:
        GPIO.cleanup()
    except Exception:
        pass

# --- signal handler ---
def _signal_handler(sig, frame):
    logger.info("Signal received, exiting")
    cleanup()
    sys.exit(0)

# --- GPIO callback ---
def _ir_callback(channel):
    global _last_event
    now = time.time()
    if now - _last_event < DEBOUNCE_SEC:
        return  # ignore within debounce window

    state = GPIO.input(channel)
    triggered = (state == 0) if ACTIVE_LOW else (state == 1)
    _last_event = now

    if triggered:
        logger.info(f"Obstacle detected on IR1 (GPIO {channel})")
    else:
        logger.info(f"No obstacle on IR1 (GPIO {channel})")

# --- main ---
def main():
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=PUD)
    GPIO.add
