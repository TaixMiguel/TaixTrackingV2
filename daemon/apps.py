from django.apps import AppConfig

from daemon.daemonWatcher import DaemonWatcher


class DaemonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daemon'

    def ready(self):
        # DaemonWatcher().run()
        pass
