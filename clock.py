import RPi.GPIO as GPIO
import time

# Frequency in Hz
frequency = 1

# Calculate the duration of HIGH and LOW states
half_period = 1 / (2 * frequency)

# Use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)

# Set up the GPIO channels
GPIO.setup(22, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

try:
    while True:
        # Set GPIO HIGH
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(7, GPIO.LOW)
        time.sleep(half_period)

        # Set GPIO LOW
        GPIO.output(22, GPIO.LOW)
        GPIO.output(7, GPIO.HIGH)
        time.sleep(half_period)

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up on CTRL+C exit
