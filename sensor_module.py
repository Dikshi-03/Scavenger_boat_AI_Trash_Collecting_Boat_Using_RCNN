# sensors_module.py
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

class SensorsModule:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        GPIO.output(self.trig_pin, False)
        time.sleep(0.5)

    def get_distance(self):
        # Send trigger pulse
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        start = time.time()
        stop = time.time()

        # Wait for echo start
        while GPIO.input(self.echo_pin) == 0:
            start = time.time()

        # Wait for echo end
        while GPIO.input(self.echo_pin) == 1:
            stop = time.time()

        elapsed = stop - start
        distance = (elapsed * 34300) / 2  # in cm
        return distance

    def cleanup(self):
        GPIO.cleanup()
