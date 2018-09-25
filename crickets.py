#!/usr/bin/env python

import multiprocessing
import os
import random
import time

import noise


class Crickets(noise.Noise):
    def run(self):
        cricket_loop = noise.get_sound_path('cricket-loop.wav')

        procs = []
        procs.append(multiprocessing.Process(
            target=noise.loop_file, args=(cricket_loop,), kwargs={'delay': 1.1}
        ))

        for x in [1, 2, 3]:
            path = noise.get_sound_path('cricket-{}.wav'.format(x))
            procs.append(multiprocessing.Process(target=self.random_crickets, args=(path,)))

        for proc in procs:
            proc.start()

        for proc in procs:
            proc.join()

    def random_crickets(self, path):
        while True:
            time.sleep(random.random() * 15)
            noise.play_file(path)

if __name__ == '__main__':
    os.setsid()
    Crickets().run()
