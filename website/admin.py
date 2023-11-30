from django.contrib import admin

from .models import Hospital, Patient, MedicalHistory, Disease, Medicine, Doctor, DocSits, PatientHospitalEvaluation, Schedule, Appointment, Payment, HospitalRoom

admin.site.register(Hospital)
admin.site.register(Patient)
admin.site.register(MedicalHistory)
admin.site.register(Disease)
admin.site.register(Medicine)
admin.site.register(Doctor)
admin.site.register(DocSits)
admin.site.register(PatientHospitalEvaluation)
admin.site.register(Schedule)
admin.site.register(Appointment)
admin.site.register(Payment)
admin.site.register(HospitalRoom)