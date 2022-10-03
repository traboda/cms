from django.db import models
from django.utils import timezone


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
    'LeaveRequest',
]
