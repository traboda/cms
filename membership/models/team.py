import pytz
from django.db import models
from django.utils import timezone


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'team'
        verbose_name_plural = "Teams"
        verbose_name = "Team"

    def __str__(self):
        return str(self.name)


__all__ = [
    'Team'
]
