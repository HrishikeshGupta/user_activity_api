# Generated by Django 3.0.5 on 2020-05-02 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_activity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activities',
            name='activity_id',
        ),
    ]
