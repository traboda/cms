from django.db import models
from django.utils import timezone
import pytz


class SpecialDate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(
        'membership.Group',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    open = models.TimeField()
    close = models.TimeField()
    isClosed = models.BooleanField(default=False)

    class Meta:
        db_table = 'membership_specialdate'
        verbose_name = 'Special Date'
        verbose_name_plural = 'Special Dates'

    def __str__(self):
        return str(self.name)


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    # timings
    workingDayOpenTime = models.TimeField()
    workingDayCloseTime = models.TimeField()
    holidayOpenTime = models.TimeField()
    holidayCloseTime = models.TimeField()

    @property
    def now(self):
        tz = pytz.timezone('Asia/Kolkata')
        return timezone.now().astimezone(tz=tz)

    @property
    def today(self):
        return self.now.date()

    def is_working_today(self):
        if SpecialDate.objects.filter(date=self.today).exists():
            day = SpecialDate.objects.get(date=self.today)
            return not day.isClosed
        return True

    def get_today_schedule(self):
        if SpecialDate.objects.filter(date=self.today).exists():
            day = SpecialDate.objects.get(date=self.today)
            return day.open, day.close

        if timezone.now().date().day == 0 or timezone.now().date().day == 7:
            return self.holidayOpenTime, self.holidayCloseTime

        return self.workingDayOpenTime, self.workingDayCloseTime

    def is_bunkable(self):
        start, end = self.get_today_schedule()
        now = self.now
        # Always can bunk before start of the day for first session
        if now.hour < start.hour:
            return True
        # can also bunk afternoon for holidays
        elif start.hour < 11 and end.hour > 21 and now.hour < 13:
            return True
        return False

    def can_take_leave(self):
        start, end = self.get_today_schedule()
        now = self.now
        # Always can take leave before start of the day
        if start.hour > now.hour:
            return True
        return False

    def is_double_bunk(self):
        start, end = self.get_today_schedule()
        now = self.now
        if now.hour < start.hour:
            return False
        elif start.hour < 11 and end.hour > 21 and now.hour < 13:
            return True
        return False

    def is_scootable(self):
        start, end = self.get_today_schedule()
        now = self.now
        # for holidays, can scoot at lunch break
        if start.hour < 11 and (12 < now.hour < 13):
            return True
        # for holidays and working days, can scoot at dinner break
        if end.hour > 21 and (19 < now.hour < 20):
            return True
        return False

    def is_double_scoot(self):
        start, end = self.get_today_schedule()
        now = self.now
        # for holidays, can scoot at lunch break
        if start.hour < 11 and (12 < now.hour < 13):
            return True
        # for holidays and working days, can scoot at dinner break
        if end.hour > 21 and (19 < now.hour < 20):
            return False
        return False

    class Meta:
        db_table = 'group'
        verbose_name_plural = "Groups"
        verbose_name = "Group"

    def __str__(self):
        return str(self.name)


class Hostel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    wardenName = models.CharField(max_length=100)
    wardenNumber = models.CharField(max_length=20)

    class Meta:
        db_table = 'hostel'
        verbose_name_plural = "Hostels"
        verbose_name = "Hostel"

    def __str__(self):
        return str(self.name)


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True
    )
    username = models.SlugField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    hostel = models.ForeignKey(
        'membership.Hostel',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    joinDate = models.DateField()
    exitDate = models.DateField(null=True, blank=True)
    isActive = models.BooleanField(default=True)
    gender = models.PositiveSmallIntegerField(default=1)
    telegramID = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'member'
        verbose_name_plural = "Members"
        verbose_name = "Member"

    def __str__(self):
        return str(self.name)


__all__ = [
    'Member',
]
