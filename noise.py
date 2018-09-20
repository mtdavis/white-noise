from __future__ import division

import os
import subprocess
import wave


class FileWrapper(object):
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


class Noise(object):
    def run(self):
        devnull = open(os.devnull, 'w')
        while True:
            aplay_proc = subprocess.Popen([
                'aplay',
                '--interactive',
                '--file-type=wav',
            ], stdin=subprocess.PIPE, stdout=devnull, stderr=devnull)

            wave_out = wave.open(FileWrapper(aplay_proc.stdin), 'wb')

            self.play_noise(wave_out)

            aplay_proc.wait()

    def play_noise(self, wave_out):
        raise NotImplemented

    def loop_file(self, wave_out, path):
        in_file = wave.open(path)

        framerate = in_file.getframerate()
        source_nframes = in_file.getnframes()
        source_duration = source_nframes / framerate
        loop_count = int(4 * 60 * 60 / source_duration)
        dest_nframes = loop_count * source_nframes

        frames = in_file.readframes(source_nframes)

        wave_out.setnchannels(in_file.getnchannels())
        wave_out.setsampwidth(in_file.getsampwidth())
        wave_out.setframerate(framerate)
        wave_out.setnframes(dest_nframes)

        for _ in range(loop_count):
            wave_out.writeframesraw(frames)
