from rest_framework import serializers
from issues import models


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):
    #Created_at = serializers.DateTimeField(format="%d %b %Y %H:%M")
    creator_username = serializers.CharField(source='Creator.username', read_only=True)

    class Meta:
        model = models.Comment
        #fields = '__all__'
        fields = ['id', 'Comment', 'Created_at', 'Issue', 'Creator', 'creator_username']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttachedFile
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = '__all__'


class AsignedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AsignedUser
        fields = '__all__'


class WatcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Watcher
        fields = '__all__'

class AttachedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttachedFile
        fields = '__all__'