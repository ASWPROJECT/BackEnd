from rest_framework import serializers
from issues import models


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    #Created_at = serializers.DateTimeField(format="%d %b %Y %H:%M")

    class Meta:
        model = models.Comment
        fields = '__all__'