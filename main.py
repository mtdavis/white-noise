#!/usr/bin/env python

import os
import signal
import subprocess
import time

from RPi import GPIO

import gpio

NOISES = [
    os.path.join(os.path.dirname(__file__), 'brown_noise.py'),
    os.path.join(os.path.dirname(__file__), 'crickets.py'),
]

class Main(object):
    def __init__(self):
        self.noise_index = 0
        self.noise_proc = None
        self.playing = False

        gpio.Toggle(15, self.toggle_callback)
        gpio.RotaryEncoder(24, 25, self.turn_callback)

    def toggle_callback(self):
        print 'toggle'

        if self.playing:
            self.playing = False
            self.stop_noise()
        else:
            self.playing = True
            self.start_noise()

    def turn_callback(self, clockwise):
        print 'turn'

        self.stop_noise()
        offset = 1 if clockwise else -1
        self.noise_index = (self.noise_index + offset) % len(NOISES)

        if self.playing:
            self.start_noise()

    def stop_noise(self):
        if self.noise_proc:
            print 'stopping noise'
            os.killpg(os.getpgid(self.noise_proc.pid), signal.SIGTERM)

    def start_noise(self):
        print 'starting noise'
        self.noise_proc = subprocess.Popen(
            NOISES[self.noise_index]
        )

    def run(self):
        while True:
            time.sleep(10)

if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        Main().run()
    finally:
        GPIO.cleanup()
