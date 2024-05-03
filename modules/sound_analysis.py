"""Helper functions for the website"""

import wave
from struct import unpack


import numpy as np
from numpy import log as np_log
from numpy.fft import rfft
import pyaudio
import soundfile as sf
import pyloudnorm as pyln


from .utilities import maketempfile_wav


class AudioStreamer:
    """Streams audio if stream is true, else returns nothing"""

    def __init__(self, stream: bool = False):
        self.stream = stream
        self.py_audio = pyaudio.PyAudio() if stream else None
        self.audio_stream = None

    def set_audio_stream(self, wav_file: wave.Wave_read):
        """Set the audio stream"""
        if self.stream:
            self.audio_stream = self.py_audio.open(  # type: ignore
                format=self.py_audio.get_format_from_width(wav_file.getsampwidth()),  # type: ignore
                channels=wav_file.getnchannels(),
                rate=wav_file.getframerate(),
                output=True,
            )  # type: ignore

    def write(self, data: bytes):
        """Write the data to the audio stream"""
        if self.stream:
            self.audio_stream.write(data)  # type: ignore

    def close(self):
        """Close the audio stream"""
        if self.stream:
            self.audio_stream.close()  # type: ignore
            self.py_audio.terminate()  # type: ignore


def calculate_pitch(wav_file: str, elderspeak: bool, stream: bool = False):
    """Calculate the pitch"""
    wav_file = maketempfile_wav(wav_file)
    chunk = 16384

    with wave.open(wav_file, "r") as wf:
        swidth = wf.getsampwidth()
        frame_rate = wf.getframerate()
        window = np.blackman(chunk)  # type: ignore

        audio_streamer = AudioStreamer(stream)
        audio_streamer.set_audio_stream(wf)
        data = wf.readframes(chunk)
        freqlist = []

        chunk_size = chunk * swidth
        while len(data) == chunk_size:
            # write data out to the audio stream
            audio_streamer.write(data)
            # unpack the data and times by the hamming window
            indata = np.array(unpack(f"{int(len(data) / swidth)}h", data)) * window
            # Take the fft and square each value
            fft_data = abs(rfft(indata)) ** 2
            # find the maximum
            which = fft_data[1:].argmax() + 1
            # use quadratic interpolation around the max
            if which != len(fft_data) - 1:
                y_0, y_1, y_2 = np_log(fft_data[which - 1 : which + 2 :])
                x_1 = (y_2 - y_0) * 0.5 / (2 * y_1 - y_2 - y_0)
                # find the frequency and output it
                thefreq = (which + x_1) * frame_rate / chunk
            else:
                thefreq = which * frame_rate / chunk
            freqlist.append(thefreq)  # type: ignore
            # read some more data
            data = wf.readframes(chunk)
    audio_streamer.write(data)

    if freqlist:
        freqlistavg = float(sum(freqlist) / len(freqlist))
        print(
            f"""
            Maximum: {max(freqlist):0.2f} Hz
            Minimum: {min(freqlist):0.2f} Hz
            Average: {freqlistavg:0.2f} Hz.
            """
        )
    else:
        freqlistavg = 0
        print("Geen frequentie gevonden.")

    audio_streamer.close()

    if elderspeak:
        print(
            f"De gemiddelde frequentie bij het elderspeak bestand is\
                    {round(freqlistavg, 2)} Hz."
        )
    else:
        print(
            f"De gemiddelde frequentie bij het neutrale bestand is {round(freqlistavg, 2)} Hz."
        )
    return round(freqlistavg, 2)


def calculate_loudness(wav_file: str, elderspeak: bool):
    """Calculate the loudness"""
    wav_file = maketempfile_wav(wav_file)
    data, rate = sf.read(  # type: ignore
        wav_file
    )  # load audio (with shape (samples, channels)) # type: ignore
    if len(data) < rate:
        return 0
    meter = pyln.Meter(rate)  # create BS.1770 meter
    loudness_range = meter.integrated_loudness(data)  # measure loudness # type: ignore
    if float("inf") == loudness_range:
        loudness_range = 10000
    elif float("-inf") == loudness_range:
        loudness_range = -10000

    if elderspeak:
        print(f"Het aantal decibel is: {loudness_range} bij het elderspeak bestand.")
    else:
        print(f"Het aantal decibel is: {loudness_range} bij het neutrale bestand.")
    return loudness_range
