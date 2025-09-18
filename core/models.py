from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User
class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)

# Patient
class Patient(models.Model):
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients")

    def __str__(self):
        return self.name

# HeartRate
class HeartRate(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="heart_rates")
    rate = models.PositiveIntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.rate} bpm"