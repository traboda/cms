from django.db import models
from django.utils import timezone

from membership.models.group import Group


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True
    )
    team = models.ForeignKey(
        'membership.Team',
        on_delete=models.CASCADE,
        null=True,
    )
    batch = models.PositiveSmallIntegerField(default=2024)
    username = models.SlugField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    hostel = models.ForeignKey(
        'membership.Hostel',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    joinDate = models.DateField(default=timezone.now)
    lastSeen = models.DateTimeField(null=True, blank=True)
    exitDate = models.DateField(null=True, blank=True)
    isActive = models.BooleanField(default=True)
    gender = models.PositiveSmallIntegerField(default=1)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    telegramID = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'member'
        verbose_name_plural = "Members"
        verbose_name = "Member"

    def __str__(self):
        return str(self.name)


__all__ = [
    'Member',
]

