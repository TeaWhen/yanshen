from django.db import models
from users.models import Profile

class AuthInfo(models.Model):
	type = models.CharField(max_length = 20)
	uid = models.CharField(max_length = 50)
	owner = models.ForeignKey(Profile, related_name = "conns")
	tokens = models.TextField()
