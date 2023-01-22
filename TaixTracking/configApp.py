import json
import logging
import os
from threading import Lock


class ConfigAppMeta(type):

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ConfigApp(metaclass=ConfigAppMeta):

    __configData: dict = {}
    __sw_daemon_launch: bool = False

    def __init__(self) -> None:
        path_file: str
        try:
            from TaixTracking import settings
            path_file = os.environ['CONFIG_FILE_TAIXTRACKING']
            with open(path_file, 'r') as config_file:
                self.__configData = json.load(config_file)
        except KeyError:
            logging.error('No se ha definido la variable de entorno CONFIG_FILE_TAIXTRACKING')
            logging.info('Se detiene la ejecución de la aplicación')
            quit()
        except FileNotFoundError:
            logging.error(f'No se encuentra el fichero de configuración "{path_file}"')
            logging.info('Se detiene la ejecución de la aplicación')
            quit()

    def is_daemon_launch(self) -> bool:
        return self.__sw_daemon_launch

    def set_daemon_launch(self, daemon_launch: bool) -> None:
        self.__sw_daemon_launch = daemon_launch

    def get_number_days_to_delete_user_inactive(self) -> int:
        try:
            return self.__configData['application']['days_to_delete_inactive_users']
        except KeyError:
            return 5

    def get_interval_time_search_tracking(self) -> int:
        try:
            return self.__configData['application']['interval_time_search_tracking']
        except KeyError:
            return 60
