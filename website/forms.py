from django import forms
from .models import Patient
from django.contrib.auth.forms import UserCreationForm

class PatientForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ['username', 'email', 'phone', 'age', 'name', 'gender']