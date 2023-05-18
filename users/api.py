import json
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
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            url = settings.BASE_URL + '/users/api-token-auth/'

            response = requests.post(url, data={
                'username': username,
                'password': form.cleaned_data.get('password1')
            })
            
            profile, created = Profile.objects.get_or_create(user=user)

            if response.status_code == 201:
                serializer = UserSerializer(user)
                token = response.json().get('token')                    
                response_data = {
                    'profile': serializer.data,
                    'token': token
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=response.status_code)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class EditProfileView(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def put(self, request):
        profile = None
        try:
            profile, created = Profile.objects.get_or_create(
                user=request.user
            )
        except: 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        profile.bio = request.data.get('bio')
        profile.save()
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
class ChangePictureProfileView(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def put(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response({'error': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)
        
        profile_picture = request.FILES.get('image')
        if profile_picture:
            picture = Picture()
            picture.File = profile_picture
            picture.save()
            profile.url = picture.File.url.split('?')[0]
            profile.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        
class ViewProfile(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def get(self, request):
        try:
            user = User.objects.get(username=request.user.username)
        except User.DoesNotExist:
            return Response({'error': 'No existe el usuario'}, status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            try:
                profile, created = Profile.objects.get_or_create(
                    user=user
                )
            except:
                return Response({'error': 'Error al crear el perfil'}, status=status.HTTP_400_BAD_REQUEST)
            auth_header = request.headers.get('Authorization')
            if auth_header and 'Token' in auth_header:
                token_key = auth_header.split('Token ')[1]
                print("Token:", token_key)  # Print the token key

                # Find the token in the database
                try:
                    token = Token.objects.get(key=token_key)
                except Token.DoesNotExist:
                    return Response("Invalid token", status=status.HTTP_401_UNAUTHORIZED)
                serializer = ProfileSerializer(profile)
                response_data = {
                    'profile': serializer.data,
                    'token': token.key  # Include the token in the response
                }
                return Response(response_data)
        

class ViewUsers(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def get(self, request):
        try:
            profiles = Profile.objects.all()
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = ProfileSerializer(profiles, many=True)
            return Response(serializer.data)