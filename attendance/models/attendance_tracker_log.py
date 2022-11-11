from django.db import models


class AttendanceTrackerLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    client = models.ForeignKey(
        'api.APIClient',
        on_delete=models.CASCADE
    )
    logs = models.JSONField()

    class Meta:
        unique_together = [
            ('timestamp', 'client')
        ]
        db_table = 'attendance_tracker_log'
        verbose_name_plural = "Attendance Tracker Logs"
        verbose_name = "Attendance Tracker Log"

    def __str__(self):
        return str(self.id)


__all__ = [
    'AttendanceTrackerLog',
]
