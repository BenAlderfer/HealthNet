from django.test import TestCase
from .models import *
from healthnet.models import Appointment
from datetime import datetime

# Create your tests here.


class InitializeTests:
    """
    Class used to store repeated values for ease of testing
    """
    hospital_name = "Test Hospital"
    hospital_max_num_patients = 20
    doctor_last_name = 'Doctor'
    doctor_1_first_name = '1'
    user_password = 'apple.123'
    doctor_1_username = 'doctor1'
    patient_last_name = "Patient"
    patient_1_first_name = '1'
    patient_1_username = 'patient1'
    patient_2_first_name = '2'
    patient_2_username = 'patient2'
    nurse_1_first_name = '1'
    nurse_last_name = 'Nurse'
    nurse_1_username = 'nurse1'
    hospital_admin_1_first_name = '1'
    hospital_admin_last_name = 'HospitalAdmin'
    hospital_admin_1_username = 'hospitaladmin1'
    emr_1_num_items = 3

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

        # creates test patient belonging to test doctor
        Patient.objects.create(last_name=self.patient_last_name,
                               first_name=self.patient_1_first_name,
                               dr=doctor1, username=self.patient_1_username,
                               password=self.user_password,
                               birthdate=datetime.now(),
                               hospital=hospital, pk=2)

        # creates a second test patient to be used in some tests
        Patient.objects.create(last_name=self.patient_last_name,
                               first_name=self.patient_2_first_name,
                               dr=doctor1, username=self.patient_2_username,
                               password=self.user_password,
                               birthdate=datetime.now(),
                               hospital=hospital, pk=3)

        # creates a test nurse
        Nurse.objects.create(last_name=self.nurse_last_name,
                             first_name=self.nurse_1_first_name,
                             username=self.nurse_1_username,
                             password=self.user_password,
                             hospital=hospital)

        # creates a test hospital administrator
        HospitalAdmin.objects.create(last_name=self.hospital_admin_last_name,
                                     first_name=self.hospital_admin_1_first_name,
                                     hospital=hospital,
                                     username=self.hospital_admin_1_username,
                                     password=self.user_password)


class HospitalTest(TestCase):
    """
    A class for testing the Hospital model.
    """

    def setUp(self):
        """
        calls the pre-written setup method to populate the database
        """
        InitializeTests().set_up()

        # make a few appointments
        duration_1_min = 30
        duration_2_min = 60
        duration_3_min = 15
        avg_duration = (duration_1_min + duration_2_min + duration_3_min) / 3

        patient = Patient.objects.get(
            username=InitializeTests.patient_1_username)
        doctor = Doctor.objects.get(username=InitializeTests.doctor_1_username)
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)

        Appointment.objects.create(patient=patient, doctor=doctor,
                                   hospital=hospital, date_time=datetime.now(),
                                   duration=duration_1_min)
        Appointment.objects.create(patient=patient, doctor=doctor,
                                   hospital=hospital, date_time=datetime.now(),
                                   duration=duration_1_min)
        Appointment.objects.create(patient=patient, doctor=doctor,
                                   hospital=hospital, date_time=datetime.now(),
                                   duration=duration_1_min)


    def tests_str(self):
        """
        Tests whether the hospital __str__ method correctly returns the
            hospital name.
        """

        # query the database for the selected hospital object
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)
        self.assertEqual(InitializeTests.hospital_name, hospital.__str__())

    def test_at_max_patients_false(self):
        """
        Tests whether the at_max_patients method corretly returns false when the
            hospital's number of associated patients is less than the
            hospital's maximum number of patients
        """
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)
        hospital.max_num_patients = 5
        self.assertEqual(hospital.at_max_patients(), False)

    def test_at_max_patients__equal_true(self):
        """
        Tests whether the at_max_patients method correctly returns true when the
            hospital's number of associated patients is equal to the hospital's
            maximum number of patients.
        """
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)
        hospital.max_num_patients = 2
        self.assertEqual(hospital.at_max_patients(), True)

    def test_at_max_patients_greater_true(self):
        """
        Tests whether the at_max_patients method correctly returns tru when the
            hospital's number of associated patients is greater than the
            hospital's maximum number of patients.
        """
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)
        hospital.max_num_patients = 1
        self.assertEqual(hospital.at_max_patients(), True)

    def test_get_avg_patient_visits(self):
        """
        Tests whether the get_avg_patient_visits method returns the correct
            number of average patient visits
        :return: true if the get_avg_patient_vists method returns 4 as number
            of patient visits, false otherwise
        """
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)
        self.assertEqual(hospital.get_avg_patient_visits(), 3/2)

    def test_get_avg_stay_length(self):
        """
        Tests whether the get_avg_stay_length method returns the correct length
            of appointments
        :return: call assertEqual with a hardcoded average stay length and a
            call to hospital avg_stay_length
        """
        # TODO: implement average stay length test

    def test_get_admission_reasons(self):
        """
        Tests whether the get_admission_reasons function properly returns
        :return:
        """
        # TODO: implement common admission reason function test

        # TODO: implement get_avg_patients_per_doctor test

        # TODO: implement get_num_users test

    def test_get_num_users(self):
        """
        Tests whether the get_num_users method returns the correct number
        of users associated with the hospital
        """
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)
        self.assertEqual(hospital.get_num_users(), 5)


class DoctorTest(TestCase):
    """
    A class for testing the Doctor model.
    """
    def setUp(self):
        """
        calls the pre-written setup method to populate the database
        """
        InitializeTests().set_up()

    def test_str(self):
        """
        Tests whether the __str__ method returns the doctor's name in the
            format LastName, FirstName
        :return: call assertEqual on doctor's __str__ and the formatted name
        """

        doctor = Doctor.objects.get(username=InitializeTests.doctor_1_username)
        name = doctor.last_name + ", " + doctor.first_name
        self.assertEqual(doctor.__str__(), name)

    def test_at_max_patients(self):
        """
        Tests whether the at_max_patients method correctly returns when the
            doctor's number of patients is lower than their max number of
            patients
        :return: call assertEqual for at_max_patients for a doctor who has 2
            patients and a max num patients of 3 and False
        :return: call assertEqual for at_max_patients for a doctor who has 2
            patients and a max num patients of 2 and True
        :return: call assertEqual for at_max_patients for a doctor who has 2
            patients and a max num patients of 0 and True
        """
        doctor = Doctor.objects.get(username=InitializeTests.doctor_1_username)
        doctor.max_num_patients = 3
        self.assertEqual(doctor.at_max_patients(), False)
        doctor.max_num_patients = 2
        self.assertEqual(doctor.at_max_patients(), True)
        doctor.max_num_patients = 0
        self.assertEqual(doctor.at_max_patients(), True)


class PatientTest(TestCase):
    """
    A class for testing the Patient model.
    """
    def setUp(self):
        """
        calls the pre-written setup method to populate the database
        """
        InitializeTests().set_up()

    def test_str(self):
        """
        Tests whether the __str__ method correctly returns the patient's name
            in the form LastName, FirstName
        :return: true if the __str__ method returns the patient's name in the
            correct format
        """
        patient1 = Patient.objects.get(username=
                                       InitializeTests.patient_1_username)
        name = InitializeTests.patient_last_name + ', ' + \
            InitializeTests.patient_1_first_name
        self.assertEqual(name, patient1.__str__())


class NurseTest(TestCase):
    """
    A class for testing the Nurse model.
    """

    def setUp(self):
        """
        calls the pre-written setup method to populate the database
        """
        InitializeTests().set_up()

    def test_str(self):
        """
        Tests whether the __str__ method correctly returns the nurse's name
            in the form LastName, FirstName
        :return: true if the __str__ method returns the nurse's name in the
            correct format
        """
        nurse1 = Nurse.objects.get(username=InitializeTests.nurse_1_username)
        name = InitializeTests.nurse_last_name + ', ' + \
            InitializeTests.nurse_1_first_name
        self.assertEqual(name, nurse1.__str__())


class HospitalAdminTest(TestCase):
    """
    A class for testing the HospitalAdmin model.
    """

    def setUp(self):
        """
        calls the pre-written setup method to populate the database
        """
        InitializeTests().set_up()

    def test_str(self):
        """
        Tests whether the __str__ method correctly returns the hospital admin's
            name in the form LastName, FirstName
        :return: true if __str__ returns the hospital admin's name in the
            correct form
        """
        hospitaladmin1 = HospitalAdmin.objects.get(
            username=InitializeTests.hospital_admin_1_username)
        name = InitializeTests.hospital_admin_last_name + ', ' + \
            InitializeTests.hospital_admin_1_first_name
        self.assertEqual(name, hospitaladmin1.__str__())
