# Generated by Django 2.2.6 on 2020-02-26 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='start',
        ),
    ]
