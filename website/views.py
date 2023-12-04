from django.shortcuts import render, redirect
from .models import Patient
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, PatientEditForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html', {})

def signup_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = PatientForm()

    return render(request, 'signup.html', {'form': form})


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

# Ridhwan
@login_required
def edit(request):
    user = request.user
    patient = Patient.objects.get(username=user.username)

    if request.method == 'POST':
        form = PatientEditForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            # messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = PatientEditForm(instance=patient)

    context = {'form': form}
    return render(request, 'edit.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account
        request.user.delete()
        
        # Log out the user
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('logout')  # You need to implement the 'logout' view in your project

    return render(request, 'delete.html')