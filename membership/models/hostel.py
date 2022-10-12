from django.db import models


class Hostel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    wardenName = models.CharField(max_length=100)
    wardenNumber = models.CharField(max_length=20)

    class Meta:
        db_table = 'hostel'
        verbose_name_plural = "Hostels"
        verbose_name = "Hostel"

    def __str__(self):
        return str(self.name)


__all__ = [
    'Hostel',
]
