#!/usr/bin/env python

import os
import wave

import noise


class BrownNoise(noise.Noise):
    def __init__(self):
        my_dir = os.path.dirname(__file__)
        in_file = wave.open(os.path.join(my_dir, 'brown-noise.wav'))

        # source file is 10 seconds, so with this loop count we'll play for 4 hours
        self.loop_count = 6 * 60 * 4

        super(BrownNoise, self).__init__(
            nchannels=in_file.getnchannels(),
            sampwidth=in_file.getsampwidth(),
            framerate=in_file.getframerate(),
            nframes=self.loop_count * in_file.getnframes()
        )

        self.frames = in_file.readframes(in_file.getnframes())

    def play_noise(self, wave_out):
        for _ in range(self.loop_count):
            wave_out.writeframesraw(self.frames)


if __name__ == '__main__':
    BrownNoise().run()
