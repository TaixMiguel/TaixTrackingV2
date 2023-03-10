import django
from django.contrib.auth.models import User
from django.db import models


class UserAttribute(models.Model):

    id_user_attribute = models.AutoField(primary_key=True)
    id_user_fK = models.ForeignKey(User, help_text='Identificador de usuario', on_delete=models.CASCADE)
    attribute_key = models.CharField(max_length=16, help_text='Código del atributo')
    attribute_value = models.TextField(max_length=1000, help_text="Valor del atributo")
    audit_time = models.DateTimeField('Fecha de actualización',
                                      help_text='Indica la fecha de la última actualización del atributo',
                                      default=django.utils.timezone.now)

    def get_user(self) -> User:
        return self.id_user_fK

    def __str__(self):
        return f'{self.attribute_key} => {self.attribute_value}'


class Tracking(models.Model):

    id_tracking = models.AutoField(primary_key=True)
    track_type = models.CharField(max_length=16, help_text='Código de la empresa de transporte')
    track_code = models.CharField(max_length=200, help_text='Código de seguimiento')
    id_creator_user_fK = models.ForeignKey(User, help_text='Identificador del usuario creador',
                                           on_delete=models.CASCADE)
    creation_time = models.DateTimeField('Fecha de creación', help_text='Indica la fecha de creación',
                                         default=django.utils.timezone.now)
    audit_time = models.DateTimeField('Fecha de actualización',
                                      help_text='Indica la fecha de la última actualización',
                                      default=django.utils.timezone.now)
    expiration_date = models.DateField('Fecha de vencimiento', help_text='Indica la fecha de vencimiento del paquete',
                                       null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['track_type', 'track_code'], name='unique tracking')
        ]

    def __str__(self):
        return f'{self.track_type}#{self.track_code}'


class TrackingDetail(models.Model):

    id_tracking_detail = models.AutoField(primary_key=True)
    id_tracking_fk = models.ForeignKey(Tracking, help_text='Identificador del tracking', on_delete=models.CASCADE)
    detail_head = models.CharField(max_length=200, help_text='Resumen del seguimiento')
    detail_text = models.TextField(max_length=1000, help_text='Detalle del seguimiento')
    creation_time = models.DateTimeField('Fecha de creación', help_text='Indica la fecha de creación',
                                         default=django.utils.timezone.now)
    audit_time = models.DateTimeField('Fecha de actualización',
                                      help_text='Indica la fecha de la última actualización',
                                      default=django.utils.timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_tracking_fk', 'detail_head', 'detail_text', 'audit_time'],
                                    name='unique tracking detail')
        ]

    def __str__(self):
        return f'{self.detail_head}\n{self.detail_text}\n{self.audit_time}'

    def pretty(self) -> str:
        return f'*✨ Situación de tu pedido:✨*\n' \
               f'*📦 Tracking:* {self.id_tracking_fk.track_code}\n' \
               f'*📪 Compañía:* {self.id_tracking_fk.track_type}\n' \
               f'*📝 Último estado:* {self.detail_text}\n' \
               f'{self.audit_time.strftime("%d/%m/%Y %H:%M:%S")}'


class TrackingUser(models.Model):

    id_tracking_user = models.AutoField(primary_key=True)
    id_tracking_fk = models.ForeignKey(Tracking, help_text='Identificador del tracking', on_delete=models.CASCADE)
    id_user_fK = models.ForeignKey(User, help_text='Identificador del usuario', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_tracking_fk', 'id_user_fK'], name='unique tracking-user')
        ]
