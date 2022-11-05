from django.db import models
from django.utils import timezone


class APIToken(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey('api.APIClient', on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    timestampGenerated = models.DateTimeField(default=timezone.now)

    def generate_token(self):
        from django.utils.crypto import get_random_string
        self.token = get_random_string(length=255)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.generate_token()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'api_token'
        verbose_name_plural = "API Tokens"
        verbose_name = "API Token"

    def __str__(self):
        return self.token


__all__ = [
    'APIToken',
]
