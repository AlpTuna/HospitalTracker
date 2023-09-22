# Django Medical Records Management System

This Django Medical Records Management System is a web application designed to help doctors and medical professionals manage patient records and test results efficiently. It provides features for creating patient records, adding medical records, ordering and reviewing laboratory and radiology tests, and more.

## Features

1. **User Authentication**:
   - Users can register for an account with their credentials.
   - Registered users can log in and log out securely.
   - User authentication and password encryption are implemented for security.

2. **Patient Management**:
   - Users can create and manage patient records, including personal information, medical history, and contact details.
   - Patients can be assigned to specific doctors.
  
3. **Patient Dashboard**:
   - Patients can view their medical records, test results, and appointment history.
   - Access to patient information is secured (patientID is encrypted), ensuring data privacy.

4. **Medical Records**:
   - Users can add medical records for patients, including details such as the reason for the visit, diagnosis, treatment, and notes.
   - Radiology and laboratory tests can be ordered and recorded in medical records.

5. **Test Management**:
   - Users can order laboratory and radiology tests for patients.
   - Laboratory tests include HDL, LDL, Triglycerides, Glucose, and more.
   - Radiology tests include Ultrasound, X-Ray, CT, MRI, PET, and more.
   - Test results can be added, edited, and reviewed by authorized users.

6. **Notifications**:
   - Notifications are sent to the laboratory specialists when new test orders are placed.
   - Notifications keep doctors informed about patient appointments and updates on medical records.

7. **Doctor Dashboard**:
   - Doctors can manage their patient list, view patient details, and access medical records.
   - Patient records are organized, making it easy to track patient history.

## Usage

1. Visit the landing page and register for a new account or log in with your credentials.

2. After logging in, you can:

   - Create and manage patient records.
   - Add medical records for patients, including test orders.
   - Review and update test results.
   - View notifications for new test orders and appointments.
   - Access patient and medical record details.

3. For laboratory specialists:

   - Receive notifications for new test orders.
   - Insert test results and notify the referring doctor.
