from django import forms
from django.forms import inlineformset_factory
from .models import Patient, Appointment, Payment, Schedule, Doctor, Hospital, HospitalRoom, MedicalHistory, Medicine, Disease
from django.contrib.auth.forms import UserCreationForm
# from datetime import datetime, time

class PatientForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ['username', 'email', 'phone', 'age', 'name', 'gender']

#Ridhwan's code
class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['email', 'phone', 'age', 'name', 'gender']

class DoctorForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(), to_field_name='d_nid', label='Select Doctor')

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        label = f"{obj.name} - {obj.d_nid} "
        # adding hospital info of doctor
        label += obj.get_hospital_list()
        return label



class DateForm(forms.Form):
    date = forms.ChoiceField(choices=(), widget=forms.RadioSelect, label='')
    doctor = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)
        super(DateForm, self).__init__(*args, **kwargs)

        if doctor:
            # Set the choices based on the selected doctor
            available_dates = Schedule.objects.filter(doctor=doctor).values_list('date', flat=True).distinct()
            print(available_dates)

            self.fields['date'].choices = [(date, date) for date in available_dates]
            self.fields['doctor'].initial = str(doctor.d_nid)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        doctor_id = self.cleaned_data.get('doctor_id')

        if date and doctor_id:
            # Check if the selected date is available for the selected doctor
            available_dates = Schedule.objects.filter(doctor_id=doctor_id).values_list('date', flat=True)

            if date not in available_dates:
                raise forms.ValidationError("This date is not available for the selected doctor.")

        return date


class TimeForm(forms.Form):
    time = forms.ChoiceField(choices=(), widget=forms.RadioSelect, label='')
    date = forms.CharField(widget=forms.HiddenInput(), required=False)
    doctor = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        date = kwargs.pop('date', None)
        doctor = kwargs.pop('doctor', None)
        super(TimeForm, self).__init__(*args, **kwargs)

        if date and doctor:
            # Check if the selected time is available for the selected doctor and date
            available_times = Schedule.objects.filter(doctor=doctor, date=date).exclude(
                appointment__isnull=False, appointment__status='Confirmed'
            ).values_list('start_time', flat=True)
            print(available_times)
            time_choices = [(str(time), time.strftime('%I:%M %p')) for time in available_times]
            self.fields['time'].choices = time_choices
            print(self.fields['time'].choices)

        

    # def clean_time(self):
    #     time = self.cleaned_data.get('time')
    #     date = self.cleaned_data.get('date')
    #     doctor = self.cleaned_data.get('doctor')

    #     print(time, date, doctor)
    #     # Debugging statements
    #     print("Type of selected time:", type(time))
    #     print("Selected time:", time)

    #     available_times = Schedule.objects.filter(doctor=doctor, date=date).values_list('start_time', flat=True)

    #     # Debugging statements
    #     print("Type of available times:", type(available_times))
    #     print("Available times:", available_times)

    #     if time not in available_times:
    #         raise forms.ValidationError("This time is not available for the selected doctor and date.")

    #     return time

class PaymentForm(forms.Form):
    method = forms.CharField(max_length=50, label='Transaction ID')

# class HospitalRoomBookingForm(forms.Form):
#     branch = forms.ModelChoiceField(queryset=Hospital.objects.all(), label='Select Branch', empty_label=None)

#     def __init__(self, *args, **kwargs):
#         super(HospitalRoomBookingForm, self).__init__(*args, **kwargs)
#         selected_branch = self.fields['branch'].initial
#         if selected_branch:
#             available_rooms = HospitalRoom.objects.filter(branch=selected_branch, is_available=True)
#             self.fields['room'] = forms.ModelChoiceField(queryset=available_rooms, label='Select Room')

#     def clean_branch(self):
#         branch = self.cleaned_data['branch']
#         # Update the form with available rooms based on the selected branch
#         available_rooms = HospitalRoom.objects.filter(branch=branch, is_available=True)
#         self.fields['room'] = forms.ModelChoiceField(queryset=available_rooms, label='Select Room')
#         return branch


class HospitalBranchForm(forms.Form):
    branch = forms.ModelChoiceField(queryset=Hospital.objects.all(), to_field_name='pk', label='Select Hospital Branch')

class HospitalRoomForm(forms.Form):
    room = forms.ModelChoiceField(queryset=HospitalRoom.objects.none(), label='Select Room', widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        branch = initial.get('branch')
        super(HospitalRoomForm, self).__init__(*args, **kwargs)
        if branch:
            self.fields['room'].queryset = HospitalRoom.objects.filter(branch=branch, is_available=True)

    def label_from_instance(self, obj):
        return f"Room {obj.room_no}"

#Ridhan's code
class DiseaseForm(forms.ModelForm):
    class Meta:
        model = Disease
        fields = ['disease_name']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name']

MedicalHistoryFormSet = inlineformset_factory(
    MedicalHistory,  # parent model
    Disease,         # related model
    form=DiseaseForm,
    extra=1,          # number of empty forms to display
    can_delete=True   # allows deleting existing instances
)

MedicineFormSet = inlineformset_factory(
    MedicalHistory,  # parent model
    Medicine,        # related model
    form=MedicineForm,
    extra=1,          # number of empty forms to display
    can_delete=True   # allows deleting existing instances
)

DiseaseFormSet = inlineformset_factory(
    MedicalHistory,  # parent model
    Disease,        # related model
    form=DiseaseForm,
    extra=1,          # number of empty forms to display
    can_delete=True   # allows deleting existing instances
)

class MedicalHistoryUpdateForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        exclude = ['patient']  # Add other fields if needed
