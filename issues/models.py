from django.db import models
from django.contrib.auth.models import User
from issues import choices

# Create your models here.

class Issue(models.Model):
    Subject = models.CharField(max_length=250)
    Description = models.TextField(max_length=500, null=True, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=50, choices=choices.status, null=True, blank=True)
    Type = models.CharField(max_length=50, choices=choices.type, null=True, blank=True)
    Severity = models.CharField(max_length=50, choices=choices.severity, null=True, blank=True)
    Priority = models.CharField(max_length=50, choices=choices.priority, null=True, blank=True)
    User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    DeadLine = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.Subject


class Comment(models.Model):
    Comment = models.TextField(max_length=1000)
    Created_at = models.DateTimeField(auto_now_add=True)
    Issue = models.ForeignKey(Issue, to_field='id', related_name='comments', null=False, on_delete=models.CASCADE)

class AttachedFile(models.Model):
    id = models.AutoField(primary_key=True)
    File = models.FileField(null=True, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Issue = models.ForeignKey(Issue, to_field='id', related_name='files', null=False, on_delete=models.CASCADE)
