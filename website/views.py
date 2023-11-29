from django.shortcuts import render, redirect
from .models import Patient
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html', {})

def signup_view(request):
    if request.method == 'POST':
        user = Patient.objects.create_user(
            username=request.POST['username'],  # Use the provided username
            email=request.POST['email'],
            phone=request.POST['phone'],
            age=request.POST['age'],
            name=request.POST['name'],
            gender=request.POST['gender'],
            password=request.POST['password1']
        )
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'signup.html')


def login_view(request):
    # If the user is already authenticated, redirect to the loggedin page
    if request.user.is_authenticated:
        return redirect('loggedin')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('loggedin')  # Redirect to the loggedin page if login is successful
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


def loggedin_view(request):
    return render(request, 'loggedin.html')

def profile_view(request):
    user = request.user
    patient = Patient.objects.get(username=user.username)
    context = {'patient': patient}
    return render(request, 'profile.html', context)

