import threading
import time

from TaixTracking.configApp import ConfigApp


class DaemonWatcher:

    turnOff: bool
    timeSleep: int

    def __init__(self) -> None:
        self.timeSleep = ConfigApp().get_interval_time_search_tracking() * 60

    def run(self) -> None:
        if not ConfigApp().is_daemon_launch():
            thread = threading.Thread(target=self.__turn_on, name='DaemonWatcher')
            thread.start()

    def __turn_on(self) -> None:
        self.turnOff = False
        ConfigApp().set_daemon_launch(True)

        while not self.turnOff:
            time.sleep(self.timeSleep)

    def turn_off(self) -> None:
        ConfigApp().set_daemon_launch(False)
        self.turnOff = True
