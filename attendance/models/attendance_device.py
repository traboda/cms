from django.db import models
from django.utils import timezone


class AttendanceDevice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    member = models.ForeignKey(
        'membership.Member',
        on_delete=models.CASCADE
    )
    macAddress = models.CharField(max_length=17, unique=True)
    timestampAdded = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attendance_device'
        verbose_name_plural = "Attendance Devices"
        verbose_name = "Attendance Device"

    def __str__(self):
        return self.name or f"{self.member}_{str(self.id)}"


__all__ = [
    'AttendanceDevice',
]
