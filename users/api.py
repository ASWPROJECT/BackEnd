from rest_framework.response import Response
from rest_framework import status
from issues.models import *
from issues.serializers import *
from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from users.serializers import *
from users.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.user)

        if request.user.is_authenticated:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            form = CreateUserForm()
            if request.method == 'POST':
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else: return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.user)
        if request.user.is_authenticated:
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')

                user = authenticate(request, username=username, password=password)      #Comprova si l'usuari introduit ja existeix

                if user is not None:
                    login(request,user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response('Username or password is incorrect', status=status.HTTP_401_UNAUTHORIZED)


        