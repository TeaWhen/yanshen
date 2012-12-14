from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from yanshen import settings


class Profile(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    contact_info = models.TextField()
    joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()
    USERNAME_FIELD = 'email'


class Category(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cats")
    privilege = models.TextField()


class Relationship(models.Model):
    from_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friends")
    to_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    cat_id = models.ForeignKey(Category, blank=True, null=True)
