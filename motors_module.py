# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

class MotorsModule:
    """
    left_motor_pins  = (left_fwd_pin, left_bwd_pin, left_en_pin)
    right_motor_pins = (right_fwd_pin, right_bwd_pin, right_en_pin)
    belt_motor_pins  = (belt_fwd_pin, belt_bwd_pin, belt_en_pin)

    left_inverted / right_inverted:
      - False: logical "forward" -> fwd_pin HIGH, bwd_pin LOW
      - True:  logical "forward" -> bwd_pin HIGH, fwd_pin LOW
    """

    def __init__(self,
                 left_motor_pins,
                 right_motor_pins,
                 belt_motor_pins,
                 left_inverted=False,
                 right_inverted=True,   # usually the right paddle is mirrored
                 pwm_freq=100):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        (self.left_fwd, self.left_bwd, self.left_en) = left_motor_pins
        (self.right_fwd, self.right_bwd, self.right_en) = right_motor_pins
        (self.belt_fwd, self.belt_bwd, self.belt_en) = belt_motor_pins

        self.left_inverted = left_inverted
        self.right_inverted = right_inverted

        for pin in (self.left_fwd, self.left_bwd, self.left_en,
                    self.right_fwd, self.right_bwd, self.right_en,
                    self.belt_fwd, self.belt_bwd, self.belt_en):
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        self.left_pwm = GPIO.PWM(self.left_en, pwm_freq)
        self.right_pwm = GPIO.PWM(self.right_en, pwm_freq)
        self.belt_pwm = GPIO.PWM(self.belt_en, pwm_freq)

        self.left_pwm.start(0)
        self.right_pwm.start(0)
        self.belt_pwm.start(0)

        self.stop()
        self.stop_conveyor()
    def _apply_motor(self, fwd_pin, bwd_pin, pwm, logical_dir, inverted, speed):
        speed = max(0, min(100, int(speed)))

        if logical_dir == 0:
            GPIO.output(fwd_pin, GPIO.LOW)
            GPIO.output(bwd_pin, GPIO.LOW)
            pwm.ChangeDutyCycle(0)
            return

        if logical_dir > 0:  # forward
            if not inverted:
                GPIO.output(fwd_pin, GPIO.HIGH)
                GPIO.output(bwd_pin, GPIO.LOW)
            else:
                GPIO.output(fwd_pin, GPIO.LOW)
                GPIO.output(bwd_pin, GPIO.HIGH)
        else:  # backward
            if not inverted:
                GPIO.output(fwd_pin, GPIO.LOW)
                GPIO.output(bwd_pin, GPIO.HIGH)
            else:
                GPIO.output(fwd_pin, GPIO.HIGH)
                GPIO.output(bwd_pin, GPIO.LOW)

        pwm.ChangeDutyCycle(speed)

    def forward(self, speed=80):
        self._apply_motor(self.left_fwd, self.left_bwd, self.left_pwm,  -1, self.left_inverted, speed)
        self._apply_motor(self.right_fwd, self.right_bwd, self.right_pwm, -1, self.right_inverted, speed)

    def backward(self, speed=80):
        self._apply_motor(self.left_fwd, self.left_bwd, self.left_pwm,  +1, self.left_inverted, speed)
        self._apply_motor(self.right_fwd, self.right_bwd, self.right_pwm, +1, self.right_inverted, speed)

    def turn_left(self, speed=50):
        self._apply_motor(self.left_fwd, self.left_bwd, self.left_pwm,  -1, self.left_inverted, speed)
        self._apply_motor(self.right_fwd, self.right_bwd, self.right_pwm, +1, self.right_inverted, speed)

    def turn_right(self, speed=50):
        self._apply_motor(self.left_fwd, self.left_bwd, self.left_pwm,  +1, self.left_inverted, speed)
        self._apply_motor(self.right_fwd, self.right_bwd, self.right_pwm, -1, self.right_inverted, speed)

    def stop(self):
        self._apply_motor(self.left_fwd, self.left_bwd, self.left_pwm,  0, False, 0)
        self._apply_motor(self.right_fwd, self.right_bwd, self.right_pwm, 0, False, 0)

    def run_conveyor(self, speed=100):
        GPIO.output(self.belt_fwd, GPIO.HIGH)
        GPIO.output(self.belt_bwd, GPIO.LOW)
        self.belt_pwm.ChangeDutyCycle(max(0, min(100, int(speed))))

    def stop_conveyor(self):
        GPIO.output(self.belt_fwd, GPIO.LOW)
        GPIO.output(self.belt_bwd, GPIO.LOW)
        self.belt_pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.stop()
        self.stop_conveyor()
        self.left_pwm.stop()
        self.right_pwm.stop()
        self.belt_pwm.stop()
        GPIO.cleanup()
