from django.shortcuts import render, redirect
from .models import Patient
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import PatientForm
from .models import PatientHospitalEvaluation, Hospital
from .forms import PatientHospitalEvaluationForm
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='login')  
def review_form(request):
    if request.method == 'POST':
        form = PatientHospitalEvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.patient = request.user
            evaluation.save()
            return redirect('review_success')
    else:
        form = PatientHospitalEvaluationForm()

    hospitals = Hospital.objects.all()
    return render(request, 'review_form.html', {'form': form, 'hospitals': hospitals})


def review_success(request):
    return render(request,'review_success.html')

def all_hospitals(request):
    hospitals = Hospital.objects.all()
    for hospital in hospitals:
        hospital.avg_review = hospital.average_review()

    return render(request, 'all_hospitals.html', {'hospitals': hospitals})

