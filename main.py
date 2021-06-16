import logging as log
from serialThread import SerialThread
import time
import signal
import sys


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__" :
    signal.signal(signal.SIGINT, signal_handler)

    log.debug("starting ...")

    serial = SerialThread()

    serial.start()
    serial.send_command("AT")
    time.sleep(1)
    print(serial.buffer)

    serial.stop()