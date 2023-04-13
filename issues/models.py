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
    Due_Date = models.DateTimeField(auto_now_add=True)
    Creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    DeadLine = models.DateField(null=True, blank=True)
    Block_reason = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.Subject


class Comment(models.Model):
    Comment = models.TextField(max_length=1000)
    Created_at = models.DateTimeField(auto_now_add=True)
    Issue = models.ForeignKey(Issue, to_field='id', related_name='comments', null=False, on_delete=models.CASCADE)
    Creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True)

class Activity(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(Issue, to_field='id', null=False, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=choices.activities, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_activities')

class AsignedUser(models.Model):
    User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    Issue = models.ForeignKey(Issue, to_field='id', null=False, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['User', 'Issue'], name='unique_migration_asignedUser_combination'
            )
        ]


class Watcher(models.Model):
    User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    Issue = models.ForeignKey(Issue, to_field='id', null=False, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['User', 'Issue'], name='unique_migration_watcher_combination'
            )
        ]

class AttachedFile(models.Model):
    Name = models.TextField(max_length=500, null=True, blank=True)
    File = models.FileField(null=True, blank=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Issue = models.ForeignKey(Issue, to_field='id', related_name='files', null=False, on_delete=models.CASCADE)
