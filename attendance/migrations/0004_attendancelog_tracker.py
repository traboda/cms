# Generated by Django 4.0.5 on 2022-11-05 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_alter_attendancelog_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancelog',
            name='tracker',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
