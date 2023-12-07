from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Hospital(models.Model):
    branch = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=255)
    road_no = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def address(self):
        return f"{self.road_no}, {self.city}, {self.zip_code}"

    def __str__(self):
        return self.branch

class Patient(AbstractUser):
    username = models.CharField(max_length=150, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    age = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    # evaluated_doctors = models.ManyToManyField(Doctor, through='PatientDoctorEvaluation', related_name='evaluated_by_patients')
    evaluated_hospitals = models.ManyToManyField(Hospital, through='PatientHospitalEvaluation', related_name='evaluated_by_patients')

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username', 'phone', 'name']

    def __str__(self):
        return self.username

class MedicalHistory(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['record_id', 'patient']

class Disease(models.Model):
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)
    disease_name = models.CharField(max_length=100)

class Medicine(models.Model):
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=100)


class Doctor(models.Model):
    d_nid = models.IntegerField(primary_key=True)
    speciality = models.CharField(max_length=15)
    degree = models.CharField(max_length=15)
    name = models.CharField(max_length=40)
    hospitals = models.ManyToManyField(Hospital, through='DocSits', through_fields=('doctor', 'hospital'))

    def get_hospital_list(self):
        hospital_names = [hospital.branch for hospital in self.hospitals.all()]
        return f"({', '.join(hospital_names)})"

    def __str__(self):
        return self.name

class DocSits(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    chamber_no = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.doctor.name} in {self.hospital.branch}, Chamber No: {self.chamber_no}"

class PatientHospitalEvaluation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    ratings = models.IntegerField()

    class Meta:
        unique_together = ('patient', 'hospital')

# class PatientDoctorEvaluation(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     ratings = models.IntegerField()

#     class Meta:
#         unique_together = ('patient', 'doctor')


class Schedule(models.Model):
    slot = models.AutoField(primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['doctor', 'date', 'start_time']

    def __str__(self):
        return f"{self.doctor} - Date: {self.date}, Time: {self.start_time}, Slot {self.slot}"

class Appointment(models.Model):
    a_id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True, null=True)
    username = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    d_nid = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, default='Pending')

    def calculate_total_price(self):
        if self.schedule:
            return self.schedule.consultation_fee
        return 0  # Handle the case where schedule is not available

    def __str__(self):
        return str(self.a_id)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=50, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True)


    def save(self, *args, **kwargs):
        # Override save method to calculate total price before saving
        if self.appointment:
            self.total_price = self.appointment.calculate_total_price()
        else:
            self.total_price = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.payment_id)

class HospitalRoom(models.Model):
    branch = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    room_no = models.CharField(max_length=10)
    patient = models.OneToOneField(Patient, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['branch', 'room_no'], name='unique_room')
        ]

    def __str__(self):
        return f"{self.branch} - Room No: {self.room_no}"

    