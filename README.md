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

8. ***New*** **Predict Pneumonia**
   - Doctors can now get a prediction on the X-Ray images of the patients based on a Deep Learning model trained with Tensorflow
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
  
# Images
* ![New Patients](https://github.com/AlpTuna/HospitalTracker/assets/67372150/1f69dc3b-bdfe-4ad1-af64-2ba7fc97a422)
* ![The patient exists](https://github.com/AlpTuna/HospitalTracker/assets/67372150/a253f549-8583-4e45-98b7-789594e0178d)
* ![Patient Tab](https://github.com/AlpTuna/HospitalTracker/assets/67372150/7b8d2ae2-40af-4e5b-960d-5a24fafe9fb0)
* ![New Record](https://github.com/AlpTuna/HospitalTracker/assets/67372150/aec4127f-0d98-44f3-8f4e-7e8b03f78ed9)
* ![Tests Summary ](https://github.com/AlpTuna/HospitalTracker/assets/67372150/ea2f4561-ea58-4a74-8a5a-8a1f01b76f73)
* ![Appointment Details 1](https://github.com/AlpTuna/HospitalTracker/assets/67372150/651fad8d-c49a-4178-8930-d014bb9c9b9a)
* ![Appointment Details 2](https://github.com/AlpTuna/HospitalTracker/assets/67372150/66197a5f-0a5f-40c8-853f-d2c83d7b067c)
   **Note:
      This page is only for the laboratory specialists since only the laboratory specialists are authorized to upload test results.
* ![Appointment Details 3](https://github.com/AlpTuna/HospitalTracker/assets/67372150/3fa8c0ee-8029-41ec-a559-21276e6e2b1e)
* ![Notifications Tab 2](https://github.com/AlpTuna/HospitalTracker/assets/67372150/5bade4db-8c52-49d3-a528-a3d8f17bcef6)
* ![Notifications Tab](https://github.com/AlpTuna/HospitalTracker/assets/67372150/29a38fe1-56dd-41c9-911c-4c6fb2fc2799)
* ![Test Result 1](https://github.com/AlpTuna/HospitalTracker/assets/67372150/a063e0b6-cad8-4385-bdac-73fe86bffd29)
* ![Test Result 2](https://github.com/AlpTuna/HospitalTracker/assets/67372150/11fb9642-963a-40ee-bc58-d7d15f8067a8)
