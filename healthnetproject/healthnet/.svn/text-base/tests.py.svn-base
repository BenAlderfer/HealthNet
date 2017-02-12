"""
                  (+++++++++++)
                  (++++)
               (+++)
             (+++)
            (++)
            [~]
            | | (~)  (~)  (~)    /~~~~~~~~~~~~
         /~~~~~~~~~~~~~~~~~~~~~~~  [~_~_] |    * * * /~~~~~~~~~~~|
       [|  %___________________           | |~~~~~~~~            |
         \[___] ___   ___   ___\  Team 4  | |  D-Train Software  |
      /// [___+/-+-\-/-+-\-/-+ \\_________|=|____________________|
    //// @-=-@ \___/ \___/ \___/  @-==-@      @-==-@      @-==-@
 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from django.test import TestCase
from .models import *
from datetime import datetime


# Docstring template:
# 	Tests whether [method] method correctly returns [return] when [condition].
#

class InitializeTests:
    class InitializeTests:
        """
        Class used to store repeated values for ease of testing
        """
        hospital_name = "Test Hospital"
        hospital_max_num_patients = 20
        user_password = 'apple.123'
        doctor_last_name = 'Doctor'
        doctor_1_first_name = '1'
        doctor_1_username = 'doctor1'
        patient_last_name = "Patient"
        patient_1_first_name = '1'
        patient_1_username = 'patient1'
        patient_2_first_name = '2'
        patient_2_username = 'patient2'
        nurse_1_first_name = '1'
        nurse_last_name = 'Nurse'
        nurse_1_username = 'nurse1'
        hospital_admin_first_name = '1'
        hospital_admin_last_name = 'HospitalAdmin'
        hospital_admin_1_username = 'hospitaladmin1'
        emr_1_num_items = 0
        prescription_1_name = "Lexapro"
        prescription_1_quantity = 100
        prescription_1_dosage = 5
        prescription_1_units = "mg"

        def set_up(self):
            """
            runs the setup for each test case
            """

            # creates a test hospital
            Hospital.objects.create(name=self.hospital_name,
                                    max_num_patients=self.hospital_max_num_patients)
            hospital = Hospital.objects.get(name=self.hospital_name)

            # creates a test doctor belonging to test hospital
            Doctor.objects.create(last_name=self.doctor_last_name,
                                  first_name=self.doctor_1_first_name,
                                  username=self.doctor_1_username,
                                  password=self.user_password)
            doctor1 = Doctor.objects.get(username=self.doctor_1_username)
            doctor1.hospitals_list.add(hospital)

            # creates the first test patient
            Patient.objects.create(last_name=self.patient_last_name,
                                   first_name=self.patient_1_first_name,
                                   dr=doctor1, username=self.patient_1_username,
                                   password=self.user_password,
                                   birthdate=datetime.now(),
                                   hospital=hospital)
            patient1 = Patient.objects.get(username=self.patient_1_username)

            # creates the second test patient to be used in some tests
            Patient.objects.create(last_name=self.patient_last_name,
                                   first_name=self.patient_2_first_name,
                                   dr=doctor1, username=self.patient_2_username,
                                   password=self.user_password,
                                   birthdate=datetime.now(),
                                   hospital=hospital)

            # creates a test nurse
            Nurse.objects.create(last_name=self.nurse_last_name,
                                 first_name=self.nurse_1_first_name,
                                 username=self.nurse_1_username,
                                 password=self.user_password,
                                 hospital=hospital)

            # creates a test hospital administrator
            HospitalAdmin.objects.create(
                last_name=self.hospital_admin_last_name,
                first_name=self.hospital_admin_first_name,
                hospital=hospital,
                username=self.hospital_admin_1_username,
                password=self.user_password)


class NotificationTest(TestCase):
    """
    A class to test the Notification model.
    """
    def setUp(self):
        """
        Calls the pre-written setup function.
        """


class AppointmentTest(TestCase):
    """
    A class to test the Appointment model.
    """
    def setUp(self):
        """
        Calls the pre-written setup function.
        """