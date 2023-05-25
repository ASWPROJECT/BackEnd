from rest_framework import serializers
from issues import models
import users


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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['username']

class ActivitySerializer(serializers.ModelSerializer):
    User_username = serializers.ReadOnlyField(source='User.username')
    Creator_username = serializers.ReadOnlyField(source='Creator.username')

    class Meta:
        model = models.Activity
        fields = ['id', 'Created_at', 'Type', 'Issue', 'Creator_username', 'User_username']


class AsignedUserSerializer(serializers.ModelSerializer):
    Username = serializers.CharField(source='User.username', read_only=True)

    class Meta:
        model = models.AsignedUser
        fields = ['User','Username']


class WatcherSerializer(serializers.ModelSerializer):
    Username = serializers.CharField(source='User.username', read_only=True)

    class Meta:
        model = models.Watcher
        fields = ['User','Username']

class AttachedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AttachedFile
        fields = '__all__'


class IssueDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)
    assigned_users = AsignedUserSerializer(many=True, read_only=True)
    watchers = WatcherSerializer(many=True, read_only=True)

    class Meta:
        model = models.Issue
        fields = '__all__'