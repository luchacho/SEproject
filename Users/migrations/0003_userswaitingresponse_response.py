# Generated by Django 3.0.3 on 2020-04-07 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_userswaitingresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='userswaitingresponse',
            name='response',
            field=models.BooleanField(null=True),
        ),
    ]