# Generated by Django 2.1 on 2018-10-10 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_usersession'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersession',
            name='session_key',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
