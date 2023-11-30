from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Patient(AbstractUser):
    username = models.CharField(max_length=150, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    age = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'phone', 'name']

    def __str__(self):
        return self.username

class Doctor(models.Model):
    d_nid = models.IntegerField(primary_key=True)
    speciality = models.CharField(max_length=15)
    degree = models.CharField(max_length=15)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    a_id = models.CharField(max_length=20, primary_key=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    username = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    consultation_fee = models.CharField(max_length=30, null=True)
    d_nid = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)


    
    def __str__(self):
        return self.a_id




    # groups = models.ManyToManyField(
    #     Group,
    #     verbose_name='groups',
    #     blank=True,
    #     help_text=(
    #         'The groups this user belongs to. A user will get all permissions '
    #         'granted to each of their groups.'
    #     ),
    #     related_name='patients',  # Use 'patients' instead of 'patient_set'
    #     related_query_name='patient',
    # )
    
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     verbose_name='user permissions',
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     related_name='patients_permissions',  # Use 'patients_permissions' instead of 'patient_set'
    #     related_query_name='patient',
    # )

    