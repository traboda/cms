from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class AttendanceTracker(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(
        max_length=10,
        default='WIFI'
    )
    api_key = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def generate_api_key(self):
        if self.api_key is None or self.api_key == "":
            import string
            from random import choices

            isGenerated = False
            code = ""
            while not isGenerated:
                code = "".join(
                    choices(
                        string.ascii_uppercase + string.ascii_lowercase + string.digits,
                        k=6,
                    )
                )
                if not AttendanceTracker.objects.filter(code=code).exists():
                    isGenerated = True
            self.api_key = code
        else:
            if len(self.code) != 6:
                raise ValidationError(
                    "Invite code should be 6 chars long.",
                    code="INVALID_INVITE_CODE_LENGTH",
                )

    def save(self, *args, **kwargs):
        self.generate_api_key()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'attendance_tracker'
        verbose_name_plural = "Attendance Trackers"
        verbose_name = "Attendance Tracker"

    def __str__(self):
        return str(self.id)


__all__ = [
    'AttendanceTracker',
]
