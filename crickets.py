#!/usr/bin/env python

import os

import noise


class Crickets(noise.Noise):
    def play_noise(self, wave_out):
        my_dir = os.path.dirname(__file__)
        path = os.path.join(my_dir, 'crickets.wav')
        self.loop_file(wave_out, path)


if __name__ == '__main__':
    Crickets().run()
