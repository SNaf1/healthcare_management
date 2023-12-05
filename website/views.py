from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Patient, Appointment, Schedule, Payment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, DoctorForm, DateForm, TimeForm, PaymentForm
from django.contrib import messages
from formtools.wizard.views import SessionWizardView
from datetime import date

def home(request):
    if request.user.is_authenticated:
        return redirect('loggedin')
        
    return render(request, 'home.html', {})

def signup_view(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Signup successful. Please login with your credentials.')
            return redirect('login')
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

# def book_appointment_view(request):
#     return render(request, 'appointment.html')

def book_appointment_view(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.cleaned_data['doctor'].d_nid
            # Redirect to the date selection view with the selected doctor
            return redirect('select_date', doctor_id=doctor)
    else:
        form = DoctorForm()

    return render(request, 'book_appointment.html', {'doctor_form': form})

def select_date_view(request, doctor_id):
    doctor = get_object_or_404(Doctor, d_nid=doctor_id)

    # Get the available dates for the selected doctor
    available_dates = Schedule.objects.filter(doctor=doctor).values_list('date', flat=True)

    if request.method == 'POST':
        form = DateForm(request.POST, doctor=doctor)
        if form.is_valid():
            date = form.cleaned_data['date']
            # Redirect to the time selection view with the selected doctor and date
            return redirect('select_time', doctor_id=doctor_id, date=date)
    else:
        form = DateForm(doctor=doctor)

    return render(request, 'select_date.html', {'date_form': form, 'doctor': doctor, 'available_dates': available_dates})


def select_time_view(request, doctor_id, date):
    doctor = get_object_or_404(Doctor, d_nid=doctor_id)

    if request.method == 'POST':
        form = TimeForm(request.POST, doctor=doctor, date=date)
        if form.is_valid():
            time = form.cleaned_data['time']

            # Check if an appointment already exists for the selected date and time
            existing_appointment = Appointment.objects.filter(
                d_nid=doctor,
                schedule__date=date,
                schedule__start_time=time,
            ).first()

            if existing_appointment:
                messages.error(request, 'This appointment is already booked. Please select a different time.')
                return redirect('select_time', doctor_id=doctor_id, date=date)

            # Redirect to the payment view with the selected doctor, date, and time
            request.session['selected_doctor'] = doctor_id
            request.session['selected_date'] = date
            request.session['selected_time'] = time

            return redirect('confirm_payment', doctor_id=doctor_id, date=date, time=time)
    else:
        available_times = Schedule.objects.filter(doctor=doctor, date=date).exclude(
            appointment__isnull=False, appointment__status='Confirmed'
        ).values_list('start_time', flat=True)

        if not available_times:
            messages.error(request, 'All time slots have been booked for this date. Please select another date.')
            return redirect('select_date', doctor_id=doctor_id)

        form = TimeForm(doctor=doctor, date=date)



    # Debugging statements
    print("Doctor:", doctor)
    print("Date:", date)
    print("Available Times:", Schedule.objects.filter(doctor=doctor, date=date).values_list('start_time', flat=True))

    return render(request, 'select_time.html', {'time_form': form, 'doctor': doctor, 'date': date})

def confirm_payment_view(request, doctor_id, date, time):
    selected_doctor_id = request.session.get('selected_doctor')
    selected_date = request.session.get('selected_date')
    selected_time = request.session.get('selected_time')

    print(selected_date, selected_doctor_id, selected_time)
    if not (selected_doctor_id and selected_date and selected_time):
        # Redirect to the doctor selection page if no doctor, date, or time is selected
        return redirect('book_appointment')

    appointment = Appointment.objects.filter(
        username=request.user,
        d_nid_id=selected_doctor_id,
        schedule__date=selected_date,
        schedule__start_time=selected_time
    ).first()

    if appointment is None:
        # If the appointment doesn't exist, create a new one
        schedule = Schedule.objects.get(doctor=selected_doctor_id, date=selected_date, start_time=selected_time)
        appointment = Appointment.objects.create(username=request.user, d_nid_id=selected_doctor_id, schedule=schedule)


    if request.method == 'POST':
        print("POST request received")
        # Handle payment confirmation
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            print("Form is valid")
            
            # Create a Payment instance and populate its fields
            payment = Payment()
            payment.method = payment_form.cleaned_data['method']
            payment.appointment = appointment
            payment.calculate_total_price()
            payment.save()
            
            # Update appointment status to 'Confirmed'
            appointment.status = 'Confirmed'
            appointment.save()

            appointment_info = {
                    'id': appointment.a_id,
                }

            # Store the appointment information in the session
            request.session['selected_appointment'] = appointment_info
            # request.session['payment'] = payment

            return redirect('appointment_success')
        else:
            print("Form is invalid")
            print(payment_form.errors)
    else:
        payment_form = PaymentForm()

    return render(request, 'confirm_payment.html', {'payment_form': payment_form, 'appointment': appointment})


def appointment_success_view(request):
    appointment_info = request.session.get('selected_appointment')

# Reconstruct the Appointment object
    appointment = Appointment.objects.get(a_id=appointment_info['id'])
    # payment = request.session.get('payment')

    return render(request, 'appointment_success.html', {'appointment': appointment})

