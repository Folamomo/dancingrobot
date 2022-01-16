import logging
import time
import math
from animation.animation_clip import AnimationClip
from servo import Servo


EXECUTORS = {}
EXECUTORS['rightThigh'] = Servo(27, -1, 0, -math.pi/4, math.pi/4)
EXECUTORS['rightShin'] = Servo(22, -1, 0, -math.pi/4, math.pi/4)

def animator_thread_func(thread_name, settings, quit_flag):
    logging.info("%s: starting", thread_name)
    animation_database = {}
    animation_database['general'] = [ AnimationClip.from_csv('anim/Armature_TestDance.csv') ]
    category = 'general'
    current_clip_idx = 0

    progress = 0

    try:
        while not quit_flag:
            logging.info("Resampling animation...")

            clip = animation_database[category][current_clip_idx]
            frame = clip.sample(progress)

            for (name, value) in frame.values.items():
                if name not in EXECUTORS:
                    continue
                
                executor = EXECUTORS[name]
                print(f"{name}: {angle}")

                executor.set(angle)

            progress = (progress + 0.03) % 1

            time.sleep(0.1)
    finally:
        # cleanup
        logging.info("%s: finishing", thread_name)

