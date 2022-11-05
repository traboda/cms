from django.db import models


class APIClient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    # Permissions - 0 - nothing, 1 - View, 2 - Edit/Add, 3 - Delete

    attendance = models.PositiveSmallIntegerField(default=0)
    members = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'api_client'
        verbose_name_plural = "API Clients"
        verbose_name = "API Client"

    def __str__(self):
        return self.name


__all__ = [
    'APIClient',
]
