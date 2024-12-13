# Generated by Django 5.1.4 on 2024-12-12 20:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoTickets', '0006_alter_usuario_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='password',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(blank=True, max_length=20, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$')]),
        ),
    ]
