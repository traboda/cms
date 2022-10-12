import pytz
from django.db import models
from django.utils import timezone

from membership.models.special_date import SpecialDate


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


__all__ = ['Group']
