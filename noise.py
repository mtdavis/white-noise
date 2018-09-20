from __future__ import division

import os
import subprocess
import time
import wave


class Noise(object):
    def run(self):
        raise NotImplemented


class AplayStdinWrapper(object):
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def tell(self):
        return 0

    def write(self, str):
        self.wrapped.write(str)

    def flush(self):
        self.wrapped.flush()

    def seek(self, offset, whence=None):
        pass


def devnull():
    return open(os.devnull, 'w')


def get_sound_path(filename):
    my_dir = os.path.dirname(__file__)
    return os.path.join(my_dir, 'sounds', filename)


def loop_file(path, delay=1):
    in_file = wave.open(path)

    framerate = in_file.getframerate()
    nchannels = in_file.getnchannels()
    sampwidth = in_file.getsampwidth()
    source_nframes = in_file.getnframes()
    source_duration = source_nframes / framerate

    # if you play a single file for more than 4-5 hours it starts sounding choppy,
    # so we'll loop the source for 4 hours, and then start a new aplay subprocess.
    # loop_count = int(4 * 60 * 60 / source_duration)
    loop_count = 1
    dest_nframes = loop_count * source_nframes

    frames = in_file.readframes(source_nframes)

    in_file.close()

    while True:
        aplay_proc = subprocess.Popen([
            'aplay',
            '--interactive',
            '--file-type=wav',
        ], stdin=subprocess.PIPE, stdout=devnull(), stderr=devnull())

        wave_out = wave.open(AplayStdinWrapper(aplay_proc.stdin), 'wb')
        wave_out.setnchannels(nchannels)
        wave_out.setsampwidth(sampwidth)
        wave_out.setframerate(framerate)
        wave_out.setnframes(dest_nframes)

        for _ in range(loop_count):
            wave_out.writeframesraw(frames)

        # minimize overlap/gap between files.
        # this amount doesn't seem to be related to aplay's buffer size.
        time.sleep(delay)


def play_file(path):
    subprocess.call([
        'aplay',
        path,
    ], stdout=devnull(), stderr=devnull())
