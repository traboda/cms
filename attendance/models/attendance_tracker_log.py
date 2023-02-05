from django.db import models


class AttendanceTrackerLog(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField()
    client = models.ForeignKey(
        'api.APIClient',
        on_delete=models.CASCADE
    )
    logs = models.JSONField()

    @property
    def totalMacs(self):
        if self.logs and 'macs' in self.logs:
            return len(self.logs['macs'])
        return 0

    @property
    def totalUsers(self):
        if self.logs and 'users' in self.logs:
            return len(self.logs['users'])
        return 0

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
