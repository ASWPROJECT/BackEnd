from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .forms import CreateUserForm
from .models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        print("REGISTER 2")
        return redirect('allIssues')
    else:
        print("REGISTER")
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
        print("la tenc petita")
        return redirect('allIssues')
    else:
        print("LOGIN")
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

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@csrf_exempt
def edit_user_profile_view(request):
    profile = None
    try:
        profile, created = Profile.objects.get_or_create(
            user=request.user
        )
        if created:
            print("Se ha creado un nuevo perfil para el usuario")
    except:
        print("Error al crear el perfil")

    if request.method == 'POST':
        profile.bio = request.POST.get('bio')
        profile.save()
        messages.success(request, 'Your profile has been updated!')

    context = {'profile': profile}
    return render(request, 'user_configuration.html', context)
