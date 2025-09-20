import RPi.GPIO as GPIO
import time

# Pin setup
IR_PIN = 17   # GPIO17 (pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_PIN, GPIO.IN)

print("IR Sensor Test - Press CTRL+C to exit")

try:
    while True:
        if GPIO.input(IR_PIN) == 0:  # Active LOW (object detected)
            print("Object Detected!")
        else:
            print("No Object")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()