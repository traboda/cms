# Generated by Django 4.0.5 on 2022-06-25 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wifiattendancedevice',
            options={'verbose_name': 'WiFi Attendance Device', 'verbose_name_plural': 'WiFi Attendance Devices'},
        ),
        migrations.AlterModelTable(
            name='wifiattendancedevice',
            table='wifi_attendance_device',
        ),
    ]