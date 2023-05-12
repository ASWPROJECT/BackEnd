from rest_framework import serializers
from users import models

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        fields = '__all__'

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Picture
        fields = '__all__'