import logging
import time
import aubio
import soundcard as sc
import numpy as np
from threading import Lock


# constants
samplerate = 44100
win_s = 512
hop_s = win_s // 8

# set up audio input
# recorder = sc.default_microphone()

# create aubio pitch detection (first argument is method, "default" is
# "yinfft", can also be "yin", "mcomb", fcomb", "schmitt").
pitcher = aubio.pitch("default", win_s, hop_s, samplerate)
tempo = aubio.tempo("default", win_s, hop_s, samplerate)
onset = aubio.onset("default", win_s, hop_s, samplerate)
# set output unit (can be 'midi', 'cent', 'Hz', ...)
pitcher.set_unit("Hz")
# ignore frames under this level (dB)
pitcher.set_silence(-40)

bpm = 120
bpm_lock = Lock()
def set_latest_bpm(value):
    bpm_lock.acquire()
    bpm = value
    bpm_lock.release()
def get_latest_bpm():
    bpm_lock.acquire()
    try:
        return bpm
    finally:
        bpm_lock.release()


def audio_analysis_thread_func(thread_name, settings, quit_flag):
    logging.info("%s: starting", thread_name)

    device_settings = settings['inputAudioDevice']
    look_in_loopback_category = device_settings['loopback']
    device_name = device_settings['name']

    try:
        try:
            mic = sc.get_microphone(device_name, look_in_loopback_category)
        except IndexError as e:
            print(f"Couldn't find \"{device_name}\" input audio device. Here's a list of system devices:")

            for device in sc.all_microphones(True):
                print(' - {"name": "' + device.name + '", "loopback": ' + str(device.isloopback).lower() + '}')
        
            return

        logging.info("Starting to listen, press Ctrl+C to stop")
        with mic.recorder(samplerate, 1) as recorder:
            # main loop
            while not quit_flag:
                gather_audio_chunk(recorder)

    finally:
        logging.info("%s: finishing", thread_name)


def gather_audio_chunk(recorder):
    # read data from audio input
    data = recorder.record(numframes=hop_s)

    # convert data to aubio float samples
    samples = np.fromstring(data, dtype=aubio.float_type)
    # pitch of current frame
    # freq = pitcher(samples)
    t = tempo(samples)
    # print(t)
    # print(freq)
    if (t):
        b = tempo.get_bpm()
        print(b)

        set_latest_bpm(b)
    