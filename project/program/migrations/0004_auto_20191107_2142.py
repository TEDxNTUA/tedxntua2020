# Generated by Django 2.2.6 on 2019-11-07 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0003_auto_20191107_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentertranslation',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
