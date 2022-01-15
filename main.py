import soundcard as sc
import numpy as np
import aubio
import json

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

def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print('Missing \"settings.json\" file. Please provide one.')
        exit(1)
    

def main():
    settings = load_settings()

    device_settings = settings['inputAudioDevice']
    look_in_loopback_category = device_settings['loopback']
    device_name = device_settings['name']

    try:
        mic = sc.get_microphone(device_name, look_in_loopback_category)
    except IndexError as e:
        print(f"Couldn't find \"{device_name}\" input audio device. Here's a list of system devices:")

        for device in sc.all_microphones(True):
            print(' - {"name": "' + device.name + '", "loopback": ' + str(device.isloopback).lower() + '}')
        
        return

    print("Starting to listen, press Ctrl+C to stop")
    with mic.recorder(samplerate, 1) as recorder:
        # main loop
        prev = 0
        while True:
            try:
                # read data from audio input
                data = recorder.record(numframes=hop_s)

                # convert data to aubio float samples
                samples = np.frombuffer(data, dtype=aubio.float_type)
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


if __name__ == '__main__':
    main()
