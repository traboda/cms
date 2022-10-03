from django.db import models


class SpecialDate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(
        'membership.Group',
        on_delete=models.CASCADE
    )
    date = models.DateField()
    open = models.TimeField()
    close = models.TimeField()
    isClosed = models.BooleanField(default=False)

    class Meta:
        db_table = 'membership_specialdate'
        verbose_name = 'Special Date'
        verbose_name_plural = 'Special Dates'

    def __str__(self):
        return str(self.name)


__all__ = [
    'SpecialDate',
]
