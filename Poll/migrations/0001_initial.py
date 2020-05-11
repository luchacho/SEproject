# Generated by Django 3.0.5 on 2020-05-11 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('ans_one', models.CharField(max_length=30)),
                ('ans_two', models.CharField(max_length=30)),
                ('ans_three', models.CharField(max_length=30)),
                ('ans_one_votes', models.IntegerField(default=0)),
                ('ans_two_votes', models.IntegerField(default=0)),
                ('ans_three_votes', models.IntegerField(default=0)),
                ('Group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Groups.Group')),
            ],
        ),
    ]
