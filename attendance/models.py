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
    bluetoothAddress = models.CharField(max_length=50, unique=True)
    timestampAdded = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attendance_device'
        verbose_name_plural = "Attendance Devices"
        verbose_name = "Attendance Device"

    def __str__(self):
        return self.name or f"{self.member}_{str(self.id)}"


class AttendanceLog(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(
        'membership.Member',
        on_delete=models.CASCADE
    )
    type = models.CharField(
        max_length=10,
        default='WIFI'
    )
    device = models.ForeignKey(
        'attendance.AttendanceDevice',
        on_delete=models.CASCADE
    )
    ipAddress = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'attendance_log'
        verbose_name_plural = "Attendance Logs"
        verbose_name = "Attendance Log"

    def __str__(self):
        return str(self.id)


class LeaveRequest(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(
        'membership.Member',
        on_delete=models.CASCADE
    )
    category = models.CharField(max_length=25)
    description = models.TextField()
    date = models.DateField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = [
            ('member', 'date')
        ]
        db_table = 'leave_request'
        verbose_name_plural = "Leave Requests"
        verbose_name = "Leave Request"

    def __str__(self):
        return str(self.id)


__all__ = [
    'AttendanceDevice',
    'AttendanceLog',
    'LeaveRequest'
]
