from django.db import models
from yanshen import settings


class AuthInfo(models.Model):
    type = models.CharField(max_length=20)
    uid = models.CharField(max_length=50)
    uname = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    icon = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="conns")
    tokens = models.TextField()

    def __unicode__(self):
        return u'{} | {} - {} {}'.format(self.owner, self.type, self.uid, self.uname)
