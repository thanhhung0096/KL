# Generated by Django 2.0.3 on 2018-04-27 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0016_auto_20180423_0807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='data',
            name='updated_by',
        ),
        migrations.DeleteModel(
            name='Data',
        ),
    ]