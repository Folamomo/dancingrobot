import logging
import time
import math
from animation.animation_clip import AnimationClip
from servo import Servo


EXECUTORS = {}
EXECUTORS['rightThigh'] = Servo(27, 1, -0.2, -math.pi/4, math.pi/4)
EXECUTORS['rightShin'] = Servo(22, -1, 0, -math.pi/4, math.pi/4)
EXECUTORS['leftThigh'] = Servo(23, -1, 0.1, -math.pi/2, math.pi/2)
EXECUTORS['leftShin'] = Servo(24, 1, -0.1, -math.pi/4, math.pi/4)

EXECUTORS['rightForearm'] = Servo(17, -1, -0.2, -math.pi/4, math.pi/4)
EXECUTORS['rightArm'] = Servo(25, 1, -0.2, -math.pi/4, math.pi/4)
EXECUTORS['leftForearm'] = Servo(6, 1, -0.2, -math.pi/4, math.pi/4)
EXECUTORS['leftArm'] = Servo(5, -1, -0.2, -math.pi/4, math.pi/4)


def dancing_routine(thread_name, quit_flag):
    animation_database = {}
    animation_database['general'] = [ AnimationClip.from_csv('anim/Armature_TestDance.csv') ]
    category = 'general'
    current_clip_idx = 0

    progress = 0

    frequency = 10

    try:
        while not quit_flag:
            logging.info("Resampling animation...")

            clip = animation_database[category][current_clip_idx]
            frame = clip.sample(progress)

            for (name, value) in frame.values.items():
                if name not in EXECUTORS:
                    continue
                
                executor = EXECUTORS[name]
                print(f"{name}: {value}")

                executor.set(value)

            progress = (progress + 0.5/frequency) % clip.duration

            time.sleep(1/frequency)
    finally:
        # cleanup
        logging.info("%s: finishing", thread_name)


def tpose_routine(thread_name, quit_flag):
    try:
        while not quit_flag:
            logging.info("T-Posing...")

            for (name, executor) in EXECUTORS.items():
                executor.set(0)

            time.sleep(1)
    finally:
        # cleanup
        logging.info("%s: finishing", thread_name)


def animator_thread_func(thread_name, settings, quit_flag):
    logging.info("%s: starting", thread_name)

    # dancing_routine(thread_name, quit_flag)
    tpose_routine(thread_name, quit_flag)