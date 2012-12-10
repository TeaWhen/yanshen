from django.db import models

class Profile(models.Model):
	email = models.EmailField()
	password = models.CharField(max_length = 50)
	contact_info = models.TextField()
	joined = models.DateTimeField(auto_now_add = True)
	updated = models.DateTimeField()

class Category(models.Model):
	name = models.CharField(max_length = 50)
	owner = models.ForeignKey(Profile, related_name = "cats")
	privilege = models.TextField()

class Relationship(models.Model):
	from_id = models.ForeignKey(Profile, related_name = "friends")
	to_id = models.ForeignKey(Profile, related_name = "+")
	cat_id = models.ForeignKey(Category, blank = True, null = True)
