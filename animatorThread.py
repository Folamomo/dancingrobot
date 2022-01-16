import logging
import time

def animator_thread_func(thread_name, settings, quit_flag):
    logging.info("%s: starting", thread_name)

    try:
        while not quit_flag:
            logging.info("Ping...")
            time.sleep(2)
    finally:
        # cleanup
        logging.info("%s: finishing", thread_name)

