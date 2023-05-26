from rest_framework import serializers
from users import models
from django.contrib.auth.models import User

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Picture
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class UserPreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProfileSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = models.Profile
        fields = ['id', 'bio', 'url', 'user_username']