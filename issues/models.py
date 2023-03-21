from django.db import models

# Create your models here.

class Issue(models.Model):
    Subject = models.CharField(max_length=250)
    Description = models.TextField(max_length=500)
    Created_at = models.DateTimeField(auto_now_add=True)

 





