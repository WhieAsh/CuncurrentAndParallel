import threading
import time


class SleppWorker(threading.Thread):
    def __init__(self, seconds, **kwargs):
        super(SleppWorker, self).__init__(**kwargs)
        self._seconds = seconds
        self.start()

    def run(self):
        time.sleep(self._seconds)
