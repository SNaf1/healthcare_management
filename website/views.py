from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Patient, Appointment, Schedule, Payment, Hospital, HospitalRoom, MedicalHistory, Medicine, Disease, PatientHospitalEvaluation, PatientDoctorEvaluation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import PatientForm, DoctorForm, DateForm, TimeForm, PaymentForm, HospitalBranchForm, HospitalRoomForm, PatientDoctorEvaluationForm
from .forms import PatientEditForm, MedicalHistoryUpdateForm, DiseaseForm, MedicineForm, MedicineFormSet, DiseaseFormSet, PatientHospitalEvaluationForm
from django.contrib import messages
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

    return render(request, 'signup.html', {'signup_form': form})


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

    return render(request, 'login.html', {'login_form': form})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def loggedin_view(request):
    return render(request, 'loggedin.html')

def profile_view(request):
    user = request.user
    patient = Patient.objects.get(username=user.username)

    # Get the medical history for the patient
    medical_history = MedicalHistory.objects.filter(patient=user).first()

    context = {
        'patient': patient,
        'medical_history': medical_history,
    }
    return render(request, 'profile.html', context)


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


def update_medical_history(request):
    medical_history = MedicalHistory.objects.filter(patient=request.user).first()

    if not medical_history:
        # If MedicalHistory doesn't exist, create a new one
        medical_history = MedicalHistory.objects.create(patient=request.user)

    if request.method == 'POST':
        formset_disease = DiseaseFormSet(request.POST, instance=medical_history, prefix='disease')
        formset_medicine = MedicineFormSet(request.POST, instance=medical_history, prefix='medicine')
        main_form = MedicalHistoryUpdateForm(request.POST, instance=medical_history)

        if formset_disease.is_valid() and formset_medicine.is_valid() and main_form.is_valid():
            main_form.save()
            formset_disease.save()
            formset_medicine.save()

            return redirect('profile')  # Redirect to a success page

    else:
        formset_disease = DiseaseFormSet(instance=medical_history, prefix='disease')
        formset_medicine = MedicineFormSet(instance=medical_history, prefix='medicine')
        main_form = MedicalHistoryUpdateForm(instance=medical_history)

    context = {
        'formset_disease': formset_disease,
        'formset_medicine': formset_medicine,
        'main_form': main_form,
        'medical_history': medical_history,
    }

    return render(request, 'med_his_update.html', context)


@login_required
def my_appointments_view(request):
    if request.user.is_authenticated:
        # Filter appointments for the logged-in user
        appointments = Appointment.objects.filter(username=request.user)
        return render(request, 'my_appointments.html', {'appointments': appointments})
    else:
        # Redirect to login page if user not logged in
        return redirect('login')

@login_required
def delete_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, a_id=appointment_id)

    # Check if the logged-in user owns the appointment
    if request.user == appointment.username:
        appointment.delete()

    return redirect('my_appointments')

@login_required
def my_room_bookings_view(request):
    if request.user.is_authenticated:
        # Filter room bookings for the logged-in user
        room_bookings = HospitalRoom.objects.filter(patient=request.user)
        return render(request, 'my_room_bookings.html', {'room_bookings': room_bookings})
    else:
        # Redirect to login page if the user is not logged in
        return redirect('login')

@login_required
def delete_room_booking_view(request, room_id):
    room_booking = get_object_or_404(HospitalRoom, id=room_id)

    # Check if the logged-in user owns the room booking
    if request.user == room_booking.patient:
        room_booking.delete()
        messages.success(request, 'Room booking deleted successfully.')
    else:
        messages.error(request, 'You do not have permission to delete this room booking.')

    return redirect('my_room_bookings')

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
                status='Confirmed',
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


    # Debugging
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
            
            # Creating payment instance
            payment = Payment()
            payment.method = payment_form.cleaned_data['method']
            payment.appointment = appointment
            payment.save()
            
            # Update appointment status to 'Confirmed'
            appointment.status = 'Confirmed'
            appointment.save()

            appointment_info = {
                    'id': appointment.a_id,
                }

            # Storing appointment info for passsing to next step
            request.session['selected_appointment'] = appointment_info

            return redirect('appointment_success')
        else:
            print("Form is invalid")
            print(payment_form.errors)
    else:
        payment_form = PaymentForm()

    return render(request, 'confirm_payment.html', {'payment_form': payment_form, 'appointment': appointment})


def appointment_success_view(request):
    appointment_info = request.session.get('selected_appointment')
    appointment = Appointment.objects.get(a_id=appointment_info['id'])

    return render(request, 'appointment_success.html', {'appointment': appointment})

def book_hospital_room_view(request):
    branches = Hospital.objects.all()

    # Check if the patient has already booked a room
    if HospitalRoom.objects.filter(patient=request.user).exists():
        messages.error(request, 'You already have a room booked.')
        return redirect('loggedin')

    if request.method == 'POST':
        form = HospitalBranchForm(request.POST)
        if form.is_valid():
            selected_branch = form.cleaned_data['branch']
            return redirect('select_room', branch_id=selected_branch.branch)
    else:
        form = HospitalBranchForm()

    return render(request, 'book_hospital_room.html', {'branches': branches, 'form': form})



def select_room_view(request, branch_id):
    hospital_branch = get_object_or_404(Hospital, branch=branch_id)

    if request.method == 'POST':
        form = HospitalRoomForm(request.POST, initial={'branch': hospital_branch.branch})
        if form.is_valid():
            # Book the selected room
            selected_room = form.cleaned_data['room']
            selected_room.is_available = False
            selected_room.patient = request.user
            selected_room.save()
            # Redirect to booking success page
            return redirect('booking_successful', branch_id=hospital_branch.branch, room_id=selected_room.room_no)
    else:
        form = HospitalRoomForm(initial={'branch': hospital_branch.branch})

    return render(request, 'select_room.html', {'form': form, 'hospital_branch': hospital_branch})


def booking_successful_view(request, branch_id, room_id):
    hospital_branch = get_object_or_404(Hospital, branch=branch_id)
    booked_room = get_object_or_404(HospitalRoom, room_no=room_id, branch=hospital_branch)

    return render(request, 'room_booking_successful.html', {'hospital_branch': hospital_branch, 'booked_room': booked_room})


def search_doctor_view(request):
    if 'doctor_name' in request.GET:
        doctor_name = request.GET['doctor_name']
        doctors = Doctor.objects.filter(name__icontains=doctor_name)
        return render(request, 'search_doctor.html', {'doctors': doctors})
    else:
        return render(request, 'search_doctor.html', {'doctors': []})



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

def doctor_review_form(request):

    if request.method == 'POST':
        form = PatientDoctorEvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.patient = request.user  # Assuming you have a user profile model
            evaluation.save()
            return redirect('doctor_review_success')  # Redirect to a success page
    else:
        form = PatientDoctorEvaluationForm()
    doctor = Doctor.objects.all
    return render(request, 'doctor_review_form.html', {'form': form, 'doctor': doctor})

def doctor_review_success(request):
    return render(request, 'review_success.html')


def all_doctors(request):
    doctors = Doctor.objects.all()
    for doctor in doctors:
        doctor.avg_review = doctor.average_review()
    return render(request, 'all_doctors.html', {'doctors': doctors})