from django.test import TestCase
from .models import *
from healthnet.models import *
from datetime import datetime


# Create your tests here.

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
        HospitalAdmin.objects.create(last_name=self.hospital_admin_last_name,
                                     first_name=self.hospital_admin_first_name,
                                     hospital=hospital,
                                     username=self.hospital_admin_1_username,
                                     password=self.user_password)

        # creates a sample emr for patient 1 and adds items
        EMR.objects.create(patient=patient1)
        emr1 = EMR.objects.get(patient=patient1)

        EMRItem.objects.create(emr=emr1, created_by=doctor1)
        EMRItem.objects.create(emr=emr1, created_by=doctor1)
        EMRItem.objects.create(emr=emr1, created_by=doctor1)
        self.emr_1_num_items += 3

        Prescription.objects.create(name=self.prescription_1_name,
                                    quantity=self.prescription_1_quantity,
                                    dosage=self.prescription_1_dosage,
                                    units=self.prescription_1_units,
                                    emr=emr1)
        self.emr_1_num_items += 1


class EMRTest(TestCase):
    """
    A class for testing the EMR model.
    """
    def setUp(self):
        """
        calls the pre-written setup method to populate the database
        """
        InitializeTests().set_up()

    def test_num_items(self):
        """
        Tests whether the num_items function properly returns the number of
            items in the EMR
        :return: call assertEqual on EMR num_items and the hard coded number of
            EMR items
        """
        patient = Patient.objects.get(username=
                                      InitializeTests.patient_1_username)
        emr = EMR.objects.get(patient=patient)
        self.assertEqual(4, emr.num_items())

    def test_str(self):
        """
        Tests whether the __str__ function properly returns the name of the
            patient associated with the EMR
        :return: call assertEqual on EMR __str__ and formatted patient name
        """
        patient = Patient.objects.get(username=
                                      InitializeTests.patient_1_username)
        name = patient.__str__()
        emr = EMR.objects.get(patient=patient)
        self.assertEqual(name, emr.__str__())


class EMRItemTest(TestCase):
    """
    A class for testing the EMRItem model.
    """

    def setUp(self):
        """
        Calls the pre-written setup method to populate the database
        """
        InitializeTests().set_up()

    def test_creator(self):
        """
        Tests whether the creator function properly returns the name of the user
            who created the EMRITem
        :return: call assertEqual on EMRItem creator and formatted creator name
        """
        emritem = EMRItem.objects.get(pk=1)
        doctor = Doctor.objects.get(username=InitializeTests.doctor_1_username)
        self.assertEqual(emritem.creator, doctor)


class PrescriptionTest(TestCase):
    """
    A class for testing the Prescription model.
    """

    def setUp(self):
        """
        Calls the pre-written setup method to populate the database.
        """
        InitializeTests().set_up()

    def test_dosage_str(self):
        """
        Tests whether the dosage_str function properly returns the dosage of the
            Prescription
        :return: call assertEqual on Prescription dosage_str and the formatted
            dosage
        """
        prescription = Prescription.objects.get(pk=4)
        prescription_str = InitializeTests.prescription_1_dosage.__str__() + \
            " " + InitializeTests.prescription_1_units
        self.assertEqual(prescription.dosage_str(), prescription_str)


class ChangeInStatus(TestCase):
    """
    A class for testing the ChangeInStatus model.
    """
    def setUp(self):
        """
        Calls the pre-written setup method to populate the database.
        """
        InitializeTests().set_up()
        # make a new transfer object
        patient = Patient.objects.get(username=
                                      InitializeTests.patient_1_username)
        emr = EMR.objects.get(patient=patient)
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)
        doctor = Doctor.objects.get(username=InitializeTests.doctor_1_username)
        Transfer.objects.create(emr=emr, hospital=hospital, doctor=doctor,
                                created_by=doctor, pk=16)

    def test_newest_admission_or_transfer(self):
        """
        Tests whether the newest_admission_or_transfer function properly returns
            the most recent admission or transfer
        :return: call assertEqual on ChangeInStatus newest_admission_or_transfer
            and a new Admission
        :return: call assertEqual on ChangeInStatus newest_admission_or_transfer
            and a new Transfer
        """

        patient = Patient.objects.get(username=
                                      InitializeTests.patient_1_username)
        emr = EMR.objects.get(patient=patient)
        hospital = Hospital.objects.get(name=InitializeTests.hospital_name)
        doctor = Doctor.objects.get(username=InitializeTests.doctor_1_username)

        transfer = Transfer.objects.get(pk=16)
        self.assertEqual(transfer, Transfer.objects.get(pk=
                            transfer.emr.latest_transfer().pk))

        # make a new admission object
        Admission.objects.create(emr=emr, hospital=hospital, doctor=doctor,
                                 reason="EMER", created_by=doctor, pk=15)

        admission = Admission.objects.get(pk=15)
        self.assertEqual(admission.pk,
                                admission.emr.latest_admission().pk)

    def test_accept_transfer(self):
        """
        Tests whether accept_transfer properly changes the acceptance status of
            a transfer
        :return: call assertEqual on the unaccepted transfer's is_accepted field
            and False
        :return: call assertEqual on the accepted transfer's is_accepted field
            and True
        """

        transfer = Transfer.objects.get(pk=16)
        transfer.initialize(user=Doctor.objects.all()[0])
        self.assertEqual(transfer.is_accepted, False)
        transfer.accept_transfer()
        self.assertEqual(transfer.is_accepted, True)
