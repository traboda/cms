from django.db import models


class AttendanceDateLog(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(
        'membership.Member',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    logs = models.JSONField()

    @property
    def minutes(self):
        return len(self.logs if self.logs else {})

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
