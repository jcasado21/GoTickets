# Generated by Django 5.1.4 on 2024-12-12 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoTickets', '0005_ticket_total_price_usuario_password_usuario_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]