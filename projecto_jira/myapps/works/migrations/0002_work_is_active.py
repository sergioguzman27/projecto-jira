# Generated by Django 2.2.7 on 2019-11-23 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]