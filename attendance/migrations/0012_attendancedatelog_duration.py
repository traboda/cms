# Generated by Django 4.0.5 on 2023-02-05 23:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_alter_attendancedatelog_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancedatelog',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]
