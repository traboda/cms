# Generated by Django 4.0.5 on 2022-10-12 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_remove_attendancedevice_bluetoothaddress'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendancelog',
            unique_together={('device', 'timestamp')},
        ),
    ]
