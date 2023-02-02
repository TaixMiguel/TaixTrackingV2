import logging

import telegram
from django.contrib.auth.models import User
from django.db import IntegrityError
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from TaixTracking import kTaixTracking
from TaixTracking.configApp import ConfigApp
from tracking.models import Tracking, UserAttribute

logger = logging.getLogger(__name__)


def __get_user_id(update: Update) -> int:
    return update.effective_user.id


def __get_user_nick(update: Update) -> str:
    return update.effective_user.username


def __get_user_language_code(update: Update) -> str:
    return update.effective_user.language_code


def __get_user(update: Update) -> User:
    logger.debug(f'El usuario de Telegram "{__get_user_nick(update)}" se ha puesto en contacto conmigo')
    user_attribute: UserAttribute = UserAttribute.objects\
        .filter(attribute_key=kTaixTracking.User.Attribute.Telegram.USER_ID)\
        .filter(attribute_value=__get_user_id(update))

    if not user_attribute:
        nickname: str = __get_user_nick(update)
        logger.info(f'El usuario de Telegram "{nickname}" se ha puesto en contacto conmigo')
        update.message.reply_text('No atiendo peticiones de desconocidos')

        user_aux: User = User.objects.create_user(username=nickname, password=nickname)
        user_aux.is_active = False
        user_aux.save()
        logger.info(f'El usuario {__get_user_nick(update)} no existía y ha sido creado')
        UserAttribute(id_user_fK=user_aux, attribute_key=kTaixTracking.User.Attribute.Telegram.USER_ID,
                      attribute_value=__get_user_id(update)).save()
        UserAttribute(id_user_fK=user_aux, attribute_key=kTaixTracking.User.Attribute.Telegram.USER_NICK,
                      attribute_value=nickname).save()
        UserAttribute(id_user_fK=user_aux, attribute_key=kTaixTracking.User.Attribute.Telegram.USER_LANGUAGE,
                      attribute_value=__get_user_language_code(update)).save()
        return user_aux
    return user_attribute[0].id_user_fK


def command_aliexpress(update: Update, context: CallbackContext) -> None:
    user: User = __get_user(update)
    track_order: str = context.args[0]
    logger.debug(f'Petición aliexpress "{track_order}"')
    if not track_order and user.is_active:
        update.message.reply_text('No se ha indicado el código de seguimiento')
        return

    tracking: Tracking = None
    try:
        tracking = Tracking(track_type=kTaixTracking.Tracking.Types.CAINIAO, track_code=track_order,
                            id_creator_user_fK=user)
        tracking.save()
    except IntegrityError as e:
        logger.info(f'Se ha intentado dar de alta nuevamente el track "{kTaixTracking.Tracking.Types.CAINIAO}#'
                    f'{track_order}"')
        trackings = Tracking.objects.filter(track_type=kTaixTracking.Tracking.Types.CAINIAO)\
                                    .filter(track_code=track_order)
        if trackings:
            tracking = trackings[0]

    # TODO: asociar el tracking al usuario
    if user.is_active:
        update.message.reply_text('Es posible que tardes un rato en recibir una respuesta. Por favor, sé paciente.')


class Telegram:

    __updater: Updater

    def __init__(self):
        try:
            self.__updater = Updater(ConfigApp().get_value('telegram', 'token', ''), use_context=True)
        except telegram.error.InvalidToken:
            logger.info('No se ha establecido un Token válido para Telegram')

    def run(self) -> None:
        if not ConfigApp().is_telegram_launch():
            ConfigApp().set_telegram_launch(True)
            logger.debug('Se inicia el servicio de Telegram')
            self.__set_commands()
            self.__updater.start_polling()
            self.__updater.idle()

    def __set_commands(self) -> None:
        self.__updater.dispatcher.add_handler(CommandHandler('aliexpress', command_aliexpress))

    def send_message_to_tracking(self, tracking: Tracking, msg: str) -> None:
        self.send_message(tracking.id_creator_user_fK, msg)

    def send_message(self, user: User, msg: str, parse_mode=telegram.constants.PARSEMODE_MARKDOWN_V2) -> None:
        attribute_id: UserAttribute = UserAttribute.objects \
            .filter(attribute_key=kTaixTracking.User.Attribute.Telegram.USER_ID) \
            .filter(id_user_fK=user)[0]
        self.__updater.bot.send_message(chat_id=attribute_id.attribute_value, text=msg, parse_mode=parse_mode)
