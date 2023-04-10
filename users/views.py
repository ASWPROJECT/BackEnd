from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import CreateUserForm

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('allIssues')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, f"Account with username ({user}) was created successfully")
                return redirect('login')
            
        context = {'form': form}
        return render(request, 'register.html', context)
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('allIssues')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)      #Comprova si l'usuari introduit ja existeix

            if user is not None:
                login(request,user)
                return redirect('allIssues')       
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')


