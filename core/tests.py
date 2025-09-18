from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, Patient, HeartRate

class UserTests(APITestCase):
    def setUp(self):
        # Setup URLs for registration and login endpoints
        self.register_url = reverse('user-register')
        self.login_url = reverse('token_obtain_pair')

    def test_user_registration(self):
        """
        Test user registration API.
        Ensures that a new user can be created successfully,
        and that the response contains username and email fields.
        """
        data = {
            "username": "doctor1",
            "email": "doctor1@test.com",
            "password": "StrongPass123",
            "password2": "StrongPass123",
            "is_doctor": True
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)


    def test_user_login(self):
        """
        Test user login API with JWT.
        Ensures that a valid user can log in and receives
        both access and refresh tokens in response.
        """
        # First, create user
        user = User.objects.create_user(username='doctor1', password='StrongPass123', is_doctor=True)
        data = {
            "username": "doctor1",
            "password": "StrongPass123"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class PatientTests(APITestCase):
    def setUp(self):
        # Create a doctor user and authenticate with JWT
        self.user = User.objects.create_user(username='doctor1', password='StrongPass123', is_doctor=True)
        self.login_url = reverse('token_obtain_pair')
        response = self.client.post(self.login_url, {"username": "doctor1", "password": "StrongPass123"}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        self.patient_url = reverse('patient-list-create')

    def test_create_single_patient(self):
        """
        Test creating a single patient.
        Ensures that the patient is associated with the correct doctor.
        """
        data = {"name": "John Doe", "age": 45, "gender": "Male"}
        response = self.client.post(self.patient_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['doctor'], self.user.id)

    def test_create_bulk_patients(self):
        """
        Test creating multiple patients in bulk.
        Ensures that all patients are created successfully in one request.
        """
        data = [
            {"name": "Alice", "age": 30, "gender": "Female"},
            {"name": "Bob", "age": 50, "gender": "Male"}
        ]
        response = self.client.post(self.patient_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    def test_list_patients(self):
        """
        Test listing patients.
        Ensures that created patients appear in the patient list API.
        """
        # Create a patient
        Patient.objects.create(name="John Doe", age=45, gender="Male", doctor=self.user)
        response = self.client.get(self.patient_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class HeartRateTests(APITestCase):
    def setUp(self):
        # Create doctor user and authenticate
        # Create user, get JWT token, create patients
        self.user = User.objects.create_user(username='doctor1', password='StrongPass123', is_doctor=True)
        login_url = reverse('token_obtain_pair')
        response = self.client.post(login_url, {"username": "doctor1", "password": "StrongPass123"}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # Create patients
        self.patient1 = Patient.objects.create(name="John Doe", age=45, gender="Male", doctor=self.user)
        self.patient2 = Patient.objects.create(name="Jane Smith", age=38, gender="Female", doctor=self.user)

        self.heart_rate_url = reverse('heart-rate-list-create')

    def test_create_single_heart_rate(self):
        """
        Test creating a single heart rate record for a patient.
        Ensures that the heart rate value is stored and returned correctly.
        """
        data = {"patient": self.patient1.id, "rate": 78}
        response = self.client.post(self.heart_rate_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rate'], 78)

    def test_create_bulk_heart_rates(self):
        """
        Test creating multiple heart rate records in bulk.
        Ensures that heart rate records are created for multiple patients in one request.
        """
        data = [
            {"patient": self.patient1.id, "rate": 80},
            {"patient": self.patient2.id, "rate": 72},
        ]
        response = self.client.post(self.heart_rate_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    def test_list_heart_rates(self):
        """
        Test listing heart rate records.
        Ensures that existing records appear when fetching heart rate data.
        """
        HeartRate.objects.create(patient=self.patient1, rate=78)
        response = self.client.get(self.heart_rate_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
