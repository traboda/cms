from django.db import models


class AttendanceDateLog(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(
        'membership.Member',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    logs = models.JSONField()
    lastSeen = models.TimeField(null=True, blank=True)

    @property
    def minutes(self):
        return len(self.logs if self.logs else {}) * 5

    @property
    def lastSeenTimestamp(self):
        return self.lastSeenTime().isoformat()

    @property
    def formattedTime(self):
        totalMinutes = self.minutes
        hours = totalMinutes // 60
        minutes = totalMinutes % 60
        return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

    def lastSeenTime(self):
        if self.lastSeen is None:
            return None
        hours, minutes = self.lastSeen.hour, self.lastSeen.minute
        date = self.date
        from django.utils import timezone
        return timezone.datetime(
            date.year, date.month, date.day, hours, minutes, tzinfo=timezone.get_current_timezone()
        )

    class Meta:
        unique_together = [
            ('member', 'date')
        ]
        db_table = 'attendance_date_log'
        verbose_name_plural = "Attendance Date Logs"
        verbose_name = "Attendance Date Log"

    def __str__(self):
        return str(self.id)


__all__ = [
    'AttendanceDateLog',
]
