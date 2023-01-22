import logging
import threading
import time

from TaixTracking.configApp import ConfigApp


def _delete_inactive_users(num_days: int) -> None:
    from tracking.models import User
    from datetime import date, timedelta

    aux_date = date.today() - timedelta(days=num_days)
    users_to_remove = User.objects.filter(sw_allow=False, creation_time__lte=aux_date)
    if users_to_remove:
        logging.info(f'{len(users_to_remove)} usuarios a eliminar a fecha {aux_date.strftime("%m/%d/%y")}')
        users_to_remove.delete()


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

        _delete_inactive_users(ConfigApp().get_number_days_to_delete_user_inactive())

        while not self.turnOff:
            time.sleep(self.timeSleep)

    def turn_off(self) -> None:
        ConfigApp().set_daemon_launch(False)
        self.turnOff = True
