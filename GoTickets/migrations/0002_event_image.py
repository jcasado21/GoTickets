# Generated by Django 5.1.4 on 2024-12-11 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GoTickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='event_images/'),
        ),
    ]