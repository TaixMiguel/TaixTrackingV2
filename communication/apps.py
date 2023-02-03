from django.apps import AppConfig

from TaixTracking.configApp import ConfigApp


class CommunicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'communication'

    def ready(self):
        if ConfigApp().get_value_boolean('telegram', 'load', False):
            # TODO: convivir con el server de django
            from communication.telegram import Telegram
            Telegram().run()
