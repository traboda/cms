# Generated by Django 4.0.5 on 2023-02-05 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0010_alter_attendancedatelog_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendancedatelog',
            options={'verbose_name': 'Attendance Date Log', 'verbose_name_plural': 'Attendance Date Logs'},
        ),
    ]