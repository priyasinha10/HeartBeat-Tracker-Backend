# HeartBeat-Tracker-Backend
A backend system for managing patients and monitoring heart rate data
# HeartBeat-Tracker-Backend – Patient & Heart Rate Monitoring Backend

**HeartBeat-Tracker-Backend** is a Django REST Framework backend project that provides secure APIs for managing **users, patients, and heart rate monitoring**.  
It supports **JWT authentication**, **bulk data creation**, and robust validations – making it a scalable solution for healthcare data systems.

## Tech Stack
- **Framework**: Django 4.x, Django REST Framework  
- **Auth**: JWT (via `djangorestframework-simplejwt`)  
- **Database**: SQLite (default) – easily switchable to PostgreSQL/MySQL  
- **Testing**: Django `APITestCase`  

---

## Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/priyasinha10/HeartBeat-Tracker-Backend.git

2. Create Virtual Environment
python -m venv env
source env/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Apply Migrations
python manage.py makemigrations
python manage.py migrate

5. Create Superuser
python manage.py createsuperuser

6. Run Development Server
python manage.py runserver


**Test Cases****
Unit tests are included to validate all major functionalities using APITestCase.

**UserTests**

User Registration → Ensures user can register successfully and returns username/email.
User Login → Verifies correct credentials return JWT access & refresh tokens.

**PatientTests**

Create Single Patient → Tests that a doctor can create a single patient record.
Create Bulk Patients → Tests bulk creation of multiple patients in one request.
List Patients → Ensures patients created are retrievable via API.

**HeartRateTests**

Create Single Heart Rate → Tests that a patient’s heart rate can be recorded.
Create Bulk Heart Rates → Tests bulk heart rate recording for multiple patients.

**Run all Test cases:
python manage.py test


