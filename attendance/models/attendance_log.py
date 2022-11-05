from django.db import models
from django.utils import timezone


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
    tracker = models.CharField(max_length=50, null=True, blank=True)

    @property
    def data(self):
        return {
            'type': self.type,
            'device': {
                'id': self.device.id,
                'name': self.device.name,
            },
            'timestamp': self.timestamp.isoformat(),
            'tracker': self.tracker,
        }

    class Meta:
        unique_together = [
            ('device', 'timestamp')
        ]
        db_table = 'attendance_log'
        verbose_name_plural = "Attendance Logs"
        verbose_name = "Attendance Log"

    def __str__(self):
        return str(self.id)


__all__ = [
    'AttendanceLog',
]
