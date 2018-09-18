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
    def __init__(self, nchannels=1, sampwidth=2, framerate=44100, nframes=0):
        self.nchannels = nchannels
        self.sampwidth = sampwidth
        self.framerate = framerate
        self.nframes = nframes

    def run(self):
        devnull = open(os.devnull, 'w')
        while True:
            aplay_proc = subprocess.Popen([
                'aplay',
                '--interactive',
                '--file-type=wav',
            ], stdin=subprocess.PIPE, stdout=devnull, stderr=devnull)

            wave_out = wave.open(FileWrapper(aplay_proc.stdin), 'wb')

            wave_out.setnchannels(self.nchannels)
            wave_out.setsampwidth(self.sampwidth)
            wave_out.setframerate(self.framerate)
            wave_out.setnframes(self.nframes)

            self.play_noise(wave_out)

            aplay_proc.wait()


    def play_noise(self, wave_out):
        raise NotImplemented
