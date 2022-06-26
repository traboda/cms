from django.db import models
from django.utils import timezone


class WiFiAttendanceDevice(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    member = models.ForeignKey(
        'membership.Member',
        on_delete=models.CASCADE
    )
    macAddress = models.CharField(max_length=17, unique=True)
    timestampAdded = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'wifi_attendance_device'
        verbose_name_plural = "WiFi Attendance Devices"
        verbose_name = "WiFi Attendance Device"

    def __str__(self):
        return self.name or f"{self.member}_{str(self.id)}"


class WiFiAttendanceLog(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(
        'membership.Member',
        on_delete=models.CASCADE
    )
    device = models.ForeignKey(
        'attendance.WiFiAttendanceDevice',
        on_delete=models.CASCADE
    )
    ipAddress = models.GenericIPAddressField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'wifi_attendance_log'
        verbose_name_plural = "WiFi Attendance Logs"
        verbose_name = "WiFi Attendance Log"

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
    type = models.CharField(max_length=25, default='BUNK')
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
    'WiFiAttendanceDevice',
    'WiFiAttendanceLog',
    'LeaveRequest'
]
