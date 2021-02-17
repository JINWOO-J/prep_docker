#!/usr/local/bin/python3
from __future__ import print_function
import signal
import subprocess
import sys
import os
import time
from threading import Event


class GracefulInterruptHandler(object):
    def __init__(self, signals=(signal.SIGINT, signal.SIGTERM)):
        self.signals = signals
        self.original_handlers = {}

    def __enter__(self):
        self.interrupted = False
        self.released = False

        for sig in self.signals:
            self.original_handlers[sig] = signal.getsignal(sig)
            signal.signal(sig, self.handler)

        return self

    def handler(self, signum, frame):
        self.release()
        self.interrupted = True

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):
        if self.released:
            return False

        for sig in self.signals:
            signal.signal(sig, self.original_handlers[sig])

        self.released = True
        return True


def handler(signum, frame):
    print('************ [SHUTDOWN] GOT SIGNAL {}'.format(signum))
    os.system("kill -TERM $(pgrep  -f 'rabbit')")
    os.system("kill -TERM $(pgrep  -f 'loopchain')")
    time.sleep(10)
    print("***** [SHUTDOWN] delay")
    # sys.exit(1)


# signal.signal(signal.SIGTERM, handler)

wait_time = 40
with GracefulInterruptHandler() as h:
    while True:
        print('****************[SHUTDOWN] Python Handler SLEEPING')
        time.sleep(1)
        if h.interrupted:
            print('**************** [SHUTDOWN] DELAY Got signal ')
            # os.system(r'kill -TERM $(pgrep  -f "rabbit")')
            wait_time -= 1
            time.sleep(1)
            while wait_time == 0:
                print(f"***** wait_time {wait_time}")

        print('DONE')

# class GracefulKiller:
#     kill_now = False
#     def __init__(self):
#         signal.signal(signal.SIGINT, self.exit_gracefully)
#         signal.signal(signal.SIGTERM, self.exit_gracefully)
#
#     def exit_gracefully(self,signum, frame):
#         self.kill_now = True
#
#
# if __name__ == '__main__':
#     killer = GracefulKiller()
#     while True:
#         time.sleep(1)
#         print("[SHUTDOWN] doing something in a loop ...")
#     print("[SHUTDOWN] End of the program. I was killed gracefully :)")


# if __name__ == '__main__':
#     for sig in ('TERM', 'HUP', 'INT'):
#         signal.signal(getattr(signal, 'SIG'+sig), quit)
#
#     main()

# while True:
#     print('**************** Python Handler SLEEPING')
#     time.sleep(1)
#     print('DONE')

