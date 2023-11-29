from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Patient(AbstractUser):
    username = models.CharField(max_length=150, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)


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

    def __str__(self):
        return self.username