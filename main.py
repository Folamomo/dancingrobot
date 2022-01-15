import soundcard as sc
import numpy as np
import aubio
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# constants
samplerate = 44100
win_s = 512
hop_s = win_s // 16
framesize = hop_s

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

print("Starting to listen, press Ctrl+C to stop")

print(sc.all_microphones(True))
loopback = sc.get_microphone("Monitor", True)
mic = sc.get_microphone("Family", False)


with loopback.recorder(samplerate, 1) as recorder:

    # main loop
    prev = 0
    while True:
        try:
            # read data from audio input
            data = recorder.record(hop_s)

            # convert data to aubio float samples
            samples = np.fromstring(data, dtype=aubio.float_type)
            # pitch of current frame
            freq = pitcher(samples)
            t = tempo(samples)
            o = onset(samples)
            # print(t)
            # print(tempo.get_bpm())
            energy = np.sum(samples**2)/len(samples)
            # print(energy, prev)
            # if (energy - prev)/(prev + 0.00000000001) > 1:
            if (t):
                # print(tempo.get_bpm())
                print("beat", end="\t", flush=True)
            prev = energy
            # compute energy of current block
            # do something with the results
            # print("{:10.4f} {:10.4f}".format(freq, energy))
            # print(energy)
        except KeyboardInterrupt:
            print("Ctrl+C pressed, exiting")
            break


