#!/usr/bin/env python

import noise


class BrownNoise(noise.Noise):
    def run(self):
        path = noise.get_sound_path('brown-noise.wav')
        noise.loop_file(path, delay=1.33)


if __name__ == '__main__':
    BrownNoise().run()
