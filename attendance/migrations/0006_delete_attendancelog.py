# Generated by Django 4.0.5 on 2022-11-05 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_attendancedatelog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AttendanceLog',
        ),
    ]
