from django.contrib import admin

from .models import Patient, Doctor, Appointment

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)