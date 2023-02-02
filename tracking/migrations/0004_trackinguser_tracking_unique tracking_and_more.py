# Generated by Django 4.1.5 on 2023-02-02 18:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracking', '0003_alter_tracking_id_creator_user_fk_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingUser',
            fields=[
                ('id_tracking_user', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddConstraint(
            model_name='tracking',
            constraint=models.UniqueConstraint(fields=('track_type', 'track_code'), name='unique tracking'),
        ),
        migrations.AddField(
            model_name='trackinguser',
            name='id_tracking_fk',
            field=models.ForeignKey(help_text='Identificador del tracking', on_delete=django.db.models.deletion.CASCADE, to='tracking.tracking'),
        ),
        migrations.AddField(
            model_name='trackinguser',
            name='id_user_fK',
            field=models.ForeignKey(help_text='Identificador del usuario', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='trackinguser',
            constraint=models.UniqueConstraint(fields=('id_tracking_fk', 'id_user_fK'), name='unique tracking-user'),
        ),
    ]
