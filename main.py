import threading
import json
import logging
import time
from audioAnalysisThread import audio_analysis_thread_func
from animatorThread import animator_thread_func
from thread_util import Flag

LOGGING_LEVEL = logging.INFO
# LOGGING_LEVEL = logging.DEBUG


def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        print('Missing \"settings.json\" file. Please provide one.')
        exit(1)
    

def main():
    # Setting up a logger
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(
        format=format,
        level=LOGGING_LEVEL,
        datefmt="%H:%M:%S"
    )

    settings = load_settings()
    quit_flag = Flag()

    audio_analysis_thread = threading.Thread(
        target=audio_analysis_thread_func,
        args=('Audio Analysis', settings, quit_flag)
    )
    animator_thread = threading.Thread(
        target=animator_thread_func,
        args=('Animator', settings, quit_flag)
    )

    audio_analysis_thread.start()
    animator_thread.start()

    # Do main things
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Ctrl+C pressed, exiting")
    finally:
        quit_flag.set()

        logging.debug("Attempting to join threads...")
        audio_analysis_thread.join()
        animator_thread.join()


if __name__ == '__main__':
    main()
