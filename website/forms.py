from django import forms
from .models import Patient
from django.contrib.auth.forms import UserCreationForm
from .models import PatientHospitalEvaluation
from .models import Hospital
from django.core.validators import MinValueValidator, MaxValueValidator

class PatientForm(UserCreationForm):
    class Meta:
        model = Patient
        fields = ['username', 'email', 'phone', 'age', 'name', 'gender']

class PatientHospitalEvaluationForm(forms.ModelForm):
    class Meta:
        model = PatientHospitalEvaluation
        fields = ['hospital', 'ratings']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital'].queryset = Hospital.objects.all()

    # Add validators to the ratings field
    ratings = forms.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text="Please enter a rating between 0 and 5.")

