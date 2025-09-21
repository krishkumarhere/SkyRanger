import RPi.GPIO as GPIO
import time

# --- IR sensor pin ---
IR_PIN = 17  # BCM numbering (pin 11 on Pi header)

# --- GPIO setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("IR sensor test running. Press Ctrl+C to exit.")

try:
    while True:
        state = GPIO.input(IR_PIN)
        if state == 0:
            print("BIG Rand detected!")
        else:
            print("Nothing detected")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()

