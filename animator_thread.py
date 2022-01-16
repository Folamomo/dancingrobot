import logging
import time
import math
import random
from animation.animation_clip import AnimationClip
from audio_analysis_thread import get_latest_bpm
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


def apply_tpose():
    for (name, executor) in EXECUTORS.items():
        executor.set(0)


def dancing_routine(thread_name, quit_flag):
    animation_database = {}
    # For each category, only the first one is always played. The rest are picked
    # to become the first, starting from the end, with the same odds each time.
    # That means that the ones that are at the end are the most lucky.
    animation_database['general'] = [
        AnimationClip.from_csv('anim/Armature_Kalinka.csv'),
        AnimationClip.from_csv('anim/Armature_TestDance.csv'),
    ]
    category = 'general'
    current_clip_timeout = 5

    def choose_new_clip():
        nonlocal category
        nonlocal animation_database
        nonlocal current_clip_timeout

        db = animation_database[category]
        clip_index = len(db) - 1
        while clip_index > 1:
            if random.uniform(0, 1) < 0.5:
                break;
            
            clip_index -= 1

        temp = db[clip_index]
        db[clip_index] = db[0]
        db[0] = temp

        current_clip_timeout = random.randint(2, 5)


    progress = 0

    frequency = 10
    bpm = get_latest_bpm()
    progress_delta = bpm / 60 / frequency

    try:
        while not quit_flag:
            clip = animation_database[category][0]
            frame = clip.sample(progress)

            for (name, value) in frame.values.items():
                if name not in EXECUTORS:
                    continue
                
                executor = EXECUTORS[name]
                executor.set(value)

            progress = (progress + progress_delta) % clip.duration
            current_clip_timeout -= progress_delta

            if current_clip_timeout <= 0:
                choose_new_clip()

            time.sleep(1/frequency)
    finally:
        # cleanup
        logging.info("T-Posing...")
        apply_tpose()

        time.sleep(1)
        logging.info("%s: finishing", thread_name)


def tpose_routine(thread_name, quit_flag):
    try:
        while not quit_flag:
            logging.info("T-Posing...")

            apply_tpose()

            time.sleep(1)
    finally:
        # cleanup
        logging.info("%s: finishing", thread_name)


def animator_thread_func(thread_name, settings, quit_flag):
    logging.info("%s: starting", thread_name)

    dancing_routine(thread_name, quit_flag)
    # tpose_routine(thread_name, quit_flag)