# Generated by Django 2.2.1 on 2019-06-06 19:44

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('basics', '0003_auto_20190606_0234'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeBusiness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basics.TypeBusiness')),
            ],
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('direction', models.CharField(max_length=100)),
                ('telephone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basics.Category')),
                ('type_of_business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basics.TypeBusiness')),
            ],
        ),
    ]