from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.utils import timezone
from yanshen import settings
from django.core.validators import validate_email

class ProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = BaseUserManager.normalize_email(email)
        validate_email(email)
        user = self.model(email=email, is_staff=False, is_active=True, is_superuser=False,
                          joined=now, updated=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        now = timezone.now()
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser):
    objects = ProfileManager()

    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, db_index=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    contact_info = models.TextField(null=True, default='')
    joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField()

    # using upyun to store files
    avatar = models.URLField(max_length=300)

    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True,
        help_text='Specific permissions for this user.')

    USERNAME_FIELD = 'email'

    def get_absolute_url(self):
        return "/contact/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.last_name, self.first_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True


class Category(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="cats")
    privilege = models.TextField()


class Relationship(models.Model):
    from_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="friends")
    to_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    cat_id = models.ForeignKey(Category, blank=True, null=True)
