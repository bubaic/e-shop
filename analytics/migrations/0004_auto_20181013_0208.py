# Generated by Django 2.1 on 2018-10-12 20:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_usersession_session_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objectviewed',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType'),
        ),
    ]
