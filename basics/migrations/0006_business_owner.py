# Generated by Django 2.2.1 on 2019-06-06 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basics', '0005_auto_20190606_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]