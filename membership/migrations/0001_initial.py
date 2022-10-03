# Generated by Django 4.0.5 on 2022-10-03 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('workingDayOpenTime', models.TimeField()),
                ('workingDayCloseTime', models.TimeField()),
                ('holidayOpenTime', models.TimeField()),
                ('holidayCloseTime', models.TimeField()),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'db_table': 'group',
            },
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('wardenName', models.CharField(max_length=100)),
                ('wardenNumber', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Hostel',
                'verbose_name_plural': 'Hostels',
                'db_table': 'hostel',
            },
        ),
        migrations.CreateModel(
            name='SpecialDate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('open', models.TimeField()),
                ('close', models.TimeField()),
                ('isClosed', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.group')),
            ],
            options={
                'verbose_name': 'Special Date',
                'verbose_name_plural': 'Special Dates',
                'db_table': 'membership_specialdate',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.SlugField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('joinDate', models.DateField()),
                ('exitDate', models.DateField(blank=True, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('gender', models.PositiveSmallIntegerField(default=1)),
                ('telegramID', models.CharField(blank=True, max_length=255, null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.group')),
                ('hostel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.hostel')),
            ],
            options={
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
                'db_table': 'member',
            },
        ),
    ]
