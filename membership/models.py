from django.db import models


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    username = models.SlugField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    joinDate = models.DateField()
    exitDate = models.DateField(null=True, blank=True)

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
