# Hospital Management System

## Introduction

Maintaining patient records in a hospital and booking appointments can be tedious processes. This hospital management system was created to provide a user-friendly interface for both patients and hospitals. Patients can use the system to book appointments, check available doctors in a particular hospital, and more.

## Table of Contents
- [Introduction](#introduction)
- [Project Features](#project-features)
- [Usage](#usage)
  - [1. Patient Signup & Sign in](#1-patient-signup--sign-in)
  - [2. Patient Details Page](#2-patient-details-page)
  - [3. Account Edit and Deletion](#3-account-edit-and-deletion)
  - [4. Medical History](#4-medical-history)
  - [5. Doctor Information](#5-doctor-information)
  - [6. Search Doctors](#6-search-doctors)
  - [7. Save Payment ID](#7-save-payment-id)
  - [8. Doctor Reviews](#8-doctor-reviews)
  - [9. Hospital Reviews](#9-hospital-reviews)
  - [10. Schedule Appointments](#10-schedule-appointments)
  - [11. Book Hospital Rooms](#11-book-hospital-rooms)
- [Contribution](#contribution)
- [License](#license)

## Project Features

This project caters to the needs of both patients and hospitals. Some of the main features include:

Patient Side:

1. **Patient Signup & Sign in:**
   - Create a new account or sign in if you are an existing user.

2. **Patient Details Page:**
   - View and manage your personal information.

3. **Account Edit and Deletion:**
   - Modify your account details or delete your account if needed.

4. **Medical History:**
   - Add, update, or delete your medical history.

5. **Doctor Information:**
   - Access details of doctors, including reviews from other patients.

6. **Search Doctors:**
   - Find doctors based on name and check details and review.

7. **Save Payment ID:**
   - Save payment IDs for reference (No payment gateway integrated).

8. **Doctor Reviews:**
   - Contribute and read reviews to make informed decisions.

9. **Hospital Reviews:**
   - Share your feedback about hospitals.

10. **Schedule Appointments:**
    - Book appointments with your preferred doctors.

11. **Book Hospital Rooms:**
    - Reserve hospital rooms for your stay.
   
Admin Side:

1. **See all tables from the admin panel:**
   - Check all the data of the patient and alter them easily.

2. **Add Doctors and their Schedule:**
   - Directly add doctors, their attributes, and schedule.
  
3. **Manage Room Bookings**
   - Check which room is booked and make them available for booking again.
  
4. **View Payment Details**
   - View payment details of appointment bookings.

  And many more management controls.

## ER Diagram 
![ER](./diagrams/ER.png)

## Schema Diagram
![Schema](./diagrams/Schema.png)

Feel free to explore and make the most of the system!

## Clone and Setup

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>

2. **Install Dependencies:** (Preferably in a virtual environment)

   ```bash
   pip install -r requirements.txt

3. **Run Migrations:**

   ```bash
   python manage.py migrate

4. **Create a Superuser (For Admin Panel):**

   ```bash
   python manage.py createsuperuser

5. **Run the Development Server:**

   ```bash
   python manage.py runserver

5. **Explore the Web Application:**
    Open a web browser and go to http://localhost:8000/



## Contribution

Contributions are welcome! If you'd like to contribute to the development of this system.

## License

This project is licensed under the [MIT License](LICENSE).
