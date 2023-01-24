from django.apps import AppConfig


class DaemonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daemon'

    def ready(self):
        from daemon.daemonWatcher import DaemonWatcher
        DaemonWatcher().run()
