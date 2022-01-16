import soundcard as sc

for device in sc.all_microphones(True):
    print(' - {"name": "' + device.name + '", "loopback": ' + str(device.isloopback).lower() + '}')
