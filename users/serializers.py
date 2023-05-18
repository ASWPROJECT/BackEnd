from rest_framework import serializers
from users import models
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Picture
        fields = '__all__'

class UserSerializer(serializers.User):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']