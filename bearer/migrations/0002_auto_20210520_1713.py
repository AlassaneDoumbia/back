# Generated by Django 3.1.5 on 2021-05-20 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bearer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bearer_in',
            name='date_mns',
            field=models.BigIntegerField(default=None),
        ),
        migrations.AddField(
            model_name='bearer_out',
            name='date_mns',
            field=models.BigIntegerField(default=None),
        ),
    ]