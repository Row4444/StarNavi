# Generated by Django 3.1.7 on 2021-03-04 10:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
