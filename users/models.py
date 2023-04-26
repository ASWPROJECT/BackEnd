from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	image = models.ImageField(null=True)
	bio = models.TextField(max_length=500, null=True, blank=True)

	
