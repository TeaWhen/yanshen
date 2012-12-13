from django.db import models
from yansheng import settings


class AuthInfo(models.Model):
    type = models.CharField(max_length=20)
    uid = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="conns")
    tokens = models.TextField()
