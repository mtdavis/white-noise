#!/usr/bin/env python

import os

import noise


class BrownNoise(noise.Noise):
    def run(self):
        my_dir = os.path.dirname(__file__)
        path = os.path.join(my_dir, 'brown-noise.wav')
        noise.loop_file(path, delay=1.33)


if __name__ == '__main__':
    BrownNoise().run()
