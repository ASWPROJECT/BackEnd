from rest_framework.response import Response
from rest_framework import status
from issuetracker2 import settings
from users.models import *
from users.serializers import *
from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from users.serializers import *
from users.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
import requests
from rest_framework.decorators import api_view

class RegisterView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                # Make a request to the token authentication endpoint
                url = settings.BASE_URL + '/users/api-token-auth/'

                response = requests.post(url, data={
                    'username': username,
                    'password': form.cleaned_data.get('password1')
                })

                if response.status_code == 200:
                    # token = response.json().get('token')

                    serializer = UserSerializer(user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=response.status_code)
            else:
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class EditProfileView(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request):
        profile = None
        try:
            profile, created = Profile.objects.get_or_create(
                user=request.user
            )
        except: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        profile.bio = request.POST.get('bio')
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
        