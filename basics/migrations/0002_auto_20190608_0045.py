# Generated by Django 2.2.1 on 2019-06-08 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basics', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='llocation_latitude',
            new_name='location_latitude',
        ),
    ]
