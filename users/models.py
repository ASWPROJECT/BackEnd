from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='user-profile-default.png')
	bio = models.TextField(max_length=500, null=True, blank=True)
