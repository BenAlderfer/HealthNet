from django.db import models
import django.contrib.auth.models as u_models
from django.core.validators import *
from datetime import datetime, timedelta
import sys


class Hospital(models.Model):
    """
    A class for all hospitals. Inherits from the basic Django model.

    Django-generated fields:
    patients_list: List of patients associated with this hospital
    doctors_list: List of doctors associated with this hospital
    nurses_list: List of nurses associated with this hospital
    admins_list: List of admins associated with this hospital
    """

    def __str__(self):
        """
        Generate a string representation of a Hospital
        :return: the hospital name
        """
        return getattr(self, 'name')

    # Name of the hospital
    name = models.CharField("Hospital Name", max_length=70)
    max_num_patients = models.IntegerField("Maximum Number of Patients",
                                           default=1000)

    appointment_length = 30

    def get_num_patients(self):
        """
        :return: The number of patients associated with this hospital
        """
        return self.patients_list.count()

    def at_max_patients(self):
        return not self.get_num_patients() < self.max_num_patients

    get_num_patients.short_description = 'Current Number of Patients'

    def get_avg_patient_visits(self):
        """
        :return: The average number of visits per patient at this hospital
        """
        num_patients = self.get_num_patients()
        num_visits = 0

        for patient in self.patients_list.all():
            num_visits += patient.appointments_list.count()

        # Avoid div by 0 errors
        if num_patients == 0:
            return 0

        average = num_visits / num_patients

        return average

    def get_admissions_reason(self):
        """
        :return: A tuple containing the most common reason for admission, as
                 well as the number of times that reason occurred.
        """

        from emr.models import Admission

        admissions = []
        statuses = self.status_change_list.all()

        for status in statuses:
            if Admission.objects.filter(pk=status.pk):
                admissions.append(Admission.objects.get(pk=status.pk))

        counter = {'SUR': 0, 'EMER': 0, 'OBS': 0, 'OTH': 0}

        for admission in admissions:
            if admission.reason == 'SUR':
                counter['SUR'] += 1
            elif admission.reason == 'EMER':
                counter['EMER'] += 1
            elif admission.reason == 'OBS':
                counter['OBS'] += 1
            else:
                counter['OTH'] += 1

        most_common = 'Surgery'
        number = counter['SUR']

        if (counter['EMER'] > number):
            most_common = 'Emergency Care'
            number = counter['EMER']

        if (counter['OBS'] > number):
            most_common = 'Observation'
            number = counter['OBS']

        if (counter['OTH'] > number):
            most_common = 'Other'
            number = counter['OTH']

        return (most_common, number)

    def get_common_prescription(self):
        """
        :return: A tuple containing the most commonly prescribed medication
                 as well as the number of times it was prescribed.
        """

        from emr.models import Prescription

        prescriptions_list = [a for a in Prescription.objects.all()]

        to_remove = []

        for prescription in prescriptions_list:
            hospital = prescription.emr.patient.hospital
            if hospital != self:
                to_remove.append(prescription)

        for prescription in to_remove:
            prescriptions_list.remove(prescription)

        prescrip_count = {}

        for prescription in prescriptions_list:

            name = prescription.name.lower().capitalize()

            if name in prescrip_count.keys():
                prescrip_count[name] += 1
            else:
                prescrip_count[name] = 1

        common_name = ''
        common_num = 0

        for key in prescrip_count.keys():
            if prescrip_count[key] > common_num:
                common_name = key
                common_num = prescrip_count[key]

        return (common_name, common_num)

    def get_avg_patients_per_doctor(self):
        """
        :return: The average number of patients of each doctor at this hospital
        """
        num_doctors = self.doctors_list.count()
        num_patients = self.patients_list.count()

        # Avoid div by 0 errors
        if num_doctors == 0:
            return 0

        average = num_patients / num_doctors
        return average

    def get_num_users(self):
        """
        :return: The total number of users registered to this hospital
        """
        num = self.doctors_list.count() + self.patients_list.count() + \
            self.nurses_list.count() + self.admins_list.count()

        return num

    def get_avg_stay_len(self):
        """
        :return: The average admission-to-discharge time of this hospital's
                 patients
        """

        from emr.models import Discharge, Admission, Transfer

        patients = self.patients_list.all()

        num_discharges = 0
        total_length = timedelta(0)

        for patient in patients:
            items = patient.emr.emritems_list.order_by('date_time')

            # Separate out the discharges and admissions

            # get an admission
            # check if the next item is transfer or discharge
            # if discharge, time delta
            # if transfer, check if next item is admission, and time delta with
            #   that
            # add all timedeltas up to get total time
            for i in range(0,len(items)):
                if Admission.objects.filter(pk=items[i].pk).count() and \
                    Admission.objects.get(pk=items[i].pk).hospital == self:
                    if i+1 < len(items) and \
                            Discharge.objects.filter(pk=items[i+1].pk).count:
                        delta = items[i+1].date_time - items[i].date_time
                        total_length += delta
                        num_discharges += 1
                    elif i+1 < len(items) and \
                            Transfer.objects.filter(pk=items[i+1].pk).count \
                            and i+2 < len(items) and \
                            Admission.objects.filter(pk=items[i+2].pk).count:
                        delta = items[i+2].date_time - items[i].date_time
                        total_length += delta
                        num_discharges += 1

        if num_discharges:
            print(total_length)
            print(num_discharges)
            return total_length/num_discharges
        else:
            return timedelta(0)


class Doctor(u_models.User):
    """
    A class for all doctors. Inherits from the Django user model.

    Django-generated fields:
    patients_list: List of patients associated with this doctor
    nurses_list: List of nurses associated with this doctor
    """

    class Meta:
        verbose_name = "Doctor"

    def __str__(self):
        """
        Generate a string representation of a Doctor
        :return: the doctor's (formatted) name
        """
        return ', '.join((getattr(self, 'last_name'),
                          getattr(self, 'first_name')))

    @property
    def name(self):
        return self.__str__()

    # Use UserManager to get the create_user method, etc.
    manager = u_models.UserManager()

    phone = models.CharField('Phone Number', max_length=16, default=None,
                             blank=True, null=True)

    # Object of hospital doctor is assigned to
    hospitals_list = models.ManyToManyField(
        Hospital, related_name='doctors_list', blank=True, default=None
    )

    # Maximum number of patients
    max_num_patients = models.IntegerField(
        "Maximum Number of Patients", default=20
    )

    def at_max_patients(self):
        """
        Check if the doctor is at maximum patient capacity
        :return: True if at capacity, False otherwise.
        """
        if self.patients_list.count() < self.max_num_patients:
            return False
        else:
            return True

    def at_high_capacity(self):
        """
        Check if the doctor is at maximum patient capacity
        :return: True if at capacity, False otherwise.
        """
        if self.patients_list.count() > .9 * getattr(self, 'max_num_patients'):
            return True
        else:
            return False

    at_max_patients.short_description = 'At Max Patients?'
    at_max_patients.boolean = True

    def get_num_patients(self):
        """
        :return: the number of patients assigned to this doctor
        """
        return self.patients_list.count()

    get_num_patients.short_description = 'Current Number of Patients'

    def patient_list(self):
        return self.patients_list.all()

    def get_notifications(self):
        """
        :return: the list of all notifications for this doctor
        """
        from healthnet.models import Notification

        return Notification.objects.filter(receiver=self)

    get_notifications.short_description = 'List of notifications'


class Patient(u_models.User):
    """
    A class for all patients. Inherits from the Django user model.

    Django-generated fields:
    emr: The EMR associated with this patient
    """

    class Meta:
        verbose_name = "Patient"

    def __str__(self):
        """
        Generate a string representation of a Patient
        :return: the patient's (formatted) name
        """
        return ', '.join((getattr(self, 'last_name'),
                          getattr(self, 'first_name')))

    insformat = RegexValidator(r'^[a-zA-Z]{1}[a-zA-Z0-9]{12}',
                               'Must match insurance number format.')

    # Use UserManager to get the create_user method, etc.
    manager = u_models.UserManager()

    MALE = 'M'
    FEMALE = 'F'
    INTERSEX = 'I'

    # Patients can be designated as biologically male or female
    SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (INTERSEX, 'Intersex')
    )

    sex = models.CharField('Biological Sex', max_length=1, choices=SEX_CHOICES)
    gender = models.CharField('Gender', max_length=10, blank=True)
    birthdate = models.DateField('Date of Birth')

    # Insurance number; must be validated.
    insurance_num = models.CharField('Insurance Number', max_length=13,
                                     validators=[insformat])

    # Object of hospital patient is assigned to
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name='patients_list'
    )

    # Object of doctor patient is assigned to
    dr = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='patients_list',
        default=None, verbose_name="Doctor"
    )

    dr.short_description = "Doctor"

    # number could be 14 with formatting - (123) 456-7890
    phone = models.CharField('Phone Number', max_length=16, default=None,
                             blank=True, null=True)

    address = models.CharField('Address', max_length=200, default=None,
                               blank=True, null=True)

    e_first_name = models.CharField("Contact's First Name", max_length=20,
                                    default=' ', blank=True)
    e_last_name = models.CharField("Contact's Last Name", max_length=20,
                                   default=' ', blank=True)
    e_phone = models.CharField("Contact's Phone Number", max_length=15,
                               default=' ', blank=True)

    admitted = models.ForeignKey(Hospital, on_delete=models.CASCADE,
                                 related_name="admitted_list", null=True,
                                 default=None)

    admitted_dr = models.ForeignKey(Doctor, on_delete=models.CASCADE,
                                    related_name='admitted_patient_list',
                                    null=True, default=None)

    # Patients do not have notifications
    def get_notifications(self):
        return []


class Nurse(u_models.User):
    """
    A class for all nurses. Inherits from the Django user model.
    """

    class Meta:
        verbose_name = "Nurse"

    def __str__(self):
        """
        Generate a string representation of a Nurse
        :return: the nurse's (formatted) name
        """
        return ', '.join((getattr(self, 'last_name'),
                          getattr(self, 'first_name')))

    # Use UserManager to get the create_user method, etc.
    manager = u_models.UserManager()

    phone = models.CharField('Phone Number', max_length=16, default=None,
                             blank=True, null=True)

    doctors_list = models.ManyToManyField(Doctor, related_name='nurses_list')

    # Object of hospital nurse is assigned to
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name='nurses_list'
    )

    @property
    def patients_list(self):
        """
        Compile a list of all patients this nurse interacts with
        :return: A list of all related patients (no duplicates)
        """
        pset = set()
        for dr in self.doctors_list.all():
            for pat in dr.patients_list.all():
                pset.add(pat)

        plist = list(pset)

        return plist

    def get_notifications(self):
        """
        :return: the list of all notifications for this nurse
        """
        from healthnet.models import Notification

        return Notification.objects.filter(receiver=self)

    get_notifications.short_description = 'List of notifications'

    # def appointments_list(self):
    #
    #     appointments = []
    #
    #     for doc in self.doctors_list.all():
    #         appointments += list(Appointment.objects.filter(doctor=doc))
    #     appointments = \
    #         sorted(appointments, key=lambda appointment: appointment.date_time)
    #     return appointments

    # List of doctors nurse is assigned to


class HospitalAdmin(u_models.User):
    """
    A class for all Hospital Admins. Inherits from the Django user model.
    """

    class Meta:
        verbose_name = "Hospital Admin"

    phone = models.CharField('Phone Number', max_length=14,
                             default=None, blank=True, null=True)

    def __str__(self):
        """
        Generate a string representation of an Admin
        :return: the admin's (formatted) name
        """
        return ', '.join((getattr(self, 'last_name'),
                          getattr(self, 'first_name')))

    # Use UserManager to get the create_user method, etc.
    manager = u_models.UserManager()

    # Object of hospital admin is assigned to
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name='admins_list'
    )

    def get_notifications(self):
        """
        :return: the list of all notifications for this hospital admin
        """
        from healthnet.models import Notification

        return Notification.objects.filter(receiver=self)

    get_notifications.short_description = 'List of notifications'

    def add_emr_from_csv(self, filename):
        """
        Add records from a comma-separated value file
        :param filename: The filename containing csv data
        :return: A list of errors in the upload
        """

        from emr.models import Vitals, Prescription, Test, Note
        from healthnet.models import Notification
        import csv

        errors = []
        line_num = 0

        csv.register_dialect('escaped', delimiter=",", escapechar="\\")

        with open(filename, newline='') as csvfile:
            pat_reader = csv.reader(csvfile, dialect='escaped')
            for line in pat_reader:

                try:

                    line_num += 1

                    if not line:
                        continue

                    if not Patient.objects.filter(username=line[1]):
                        errors.append("Line %d: invalid username '%s'",
                                      (line_num, line[1]))
                        continue

                    if line[0] == "Vital":
                        patient = Patient.objects.get(username=line[1])
                        emr = patient.emr

                        height = float(line[2])
                        weight = float(line[3])
                        blood_pressure = line[4]
                        heart_rate = float(line[5])
                        cholesterol = float(line[6])

                        record = Vitals(emr=emr, height=height, weight=weight,
                                       heart_rate=heart_rate,
                                       cholesterol=cholesterol,
                                       blood_pressure_str=blood_pressure,
                                       is_released_to_patient=True,
                                       created_by=self,
                                       date_time=datetime.now())

                        record.save()

                        event = ChangelogEntry(
                            hospital=emr.patient.hospital,
                            time=datetime.now(),
                            generatedby=self,
                            description='Vitals Record Added for %s' \
                                        % patient.__str__()
                        )
                        event.save()

                    elif line[0] == "Prescription":

                        patient = Patient.objects.get(username=line[1])
                        emr = patient.emr

                        name = line[2]
                        quantity = line[3]
                        dosage = line[4]
                        units = line[5]

                        record = Prescription(emr=emr, name=name, quantity=quantity,
                                              dosage=dosage, units=units,
                                              is_released_to_patient=True,
                                              created_by=self,
                                              date_time=datetime.now())

                        record.save()

                        event = ChangelogEntry(
                            hospital=emr.patient.hospital,
                            time=datetime.now(),
                            generatedby=self,
                            description='Prescription Record Added for %s' \
                                        % patient.__str__()
                        )
                        event.save()


                    elif line[0] == "Test":

                        patient = Patient.objects.get(username=line[1])
                        emr = patient.emr

                        description=line[2]
                        result=line[3]
                        comments=line[4]

                        if 'f' in line[5].lower():
                            released = False
                        else:
                            released = True



                        record = Test(emr=emr, description=description,
                                      result=result, comments=comments,
                                      is_released_to_patient=released,
                                      created_by=self, date_time=datetime.now())

                        record.save()

                        if not record.is_released_to_patient:
                            notification = Notification(
                                receiver=patient.dr,
                                message='Test awaiting approval for patient: %s' % (
                                    patient.__str__()
                                ),
                                related_action='/'
                            )
                            notification.save()

                        if line[6]:

                            try:

                                # Try to open it, to make sure it's there
                                with open(line[6]) as test:
                                    pass

                                record.image.name = line[6]
                                record.save()

                            except:
                                errors.append(' '.join(
                                    ["Line %d: the specified image" % (line_num),
                                        " does not exist or has moved.",
                                        " Test has been saved with no image."]))

                        event = ChangelogEntry(
                            hospital=emr.patient.hospital,
                            time=datetime.now(),
                            generatedby=self,
                            description='Test Record Added for %s' \
                                        % patient.__str__()
                        )
                        event.save()

                    else:
                        errors.append("Line %d: invalid identifier '%s'" %
                                      (line_num, line[0]))

                except:
                    errors.append(["CSV file is invalid"])
                    break

        return errors

    def write_emr_to_csv(self, filename):
        """
        Write electronic medical records to a csv file
        :param filename: The file to write to
        """

        from emr.models import Vitals, Prescription, Test, Note
        import csv

        csv.register_dialect('escaped', delimiter=",", escapechar="\\")

        with open(filename, 'w', newline='') as csvfile:
            emr_writer = csv.writer(csvfile, dialect='escaped')

            for patient in self.hospital.patients_list.all():
                for record in Vitals.objects.filter(emr=patient.emr):

                    # Build the row
                    write_row=["Vital",]
                    write_row.append(patient.username)
                    write_row.append(record.height)
                    write_row.append(record.weight)
                    write_row.append(record.blood_pressure_str)
                    write_row.append(record.heart_rate)
                    write_row.append(record.cholesterol)

                    # And export it
                    emr_writer.writerow(write_row)

                for record in Prescription.objects.filter(emr=patient.emr):

                    # Build the row
                    write_row=["Prescription",]
                    write_row.append(patient.username)
                    write_row.append(record.name)
                    write_row.append(record.quantity)
                    write_row.append(record.dosage)
                    write_row.append(record.units)

                    # And export it
                    emr_writer.writerow(write_row)

                for record in Test.objects.filter(emr=patient.emr):

                    # Build the row
                    write_row=["Test",]
                    write_row.append(patient.username)
                    write_row.append(record.description)
                    write_row.append(record.result)
                    write_row.append(record.comments)
                    write_row.append(str(record.is_released_to_patient).lower())
                    write_row.append(record.image.name)

                    # And export it
                    emr_writer.writerow(write_row)

    def add_patients_from_csv(self, filename):
        """
        Add patients from a comma-separated value file
        :param filename: The filename containing csv data
        :return: A list of errors in the upload
        """

        from .forms import PatientForm
        import csv

        csv.register_dialect('escaped', delimiter=",", escapechar="\\")
        errors = []

        with open(filename, newline='') as csvfile:
            pat_reader = csv.reader(csvfile, dialect='escaped')
            line_num = 0

            for line in pat_reader:

                try:

                    line_num += 1

                    if not line:
                        continue

                    if u_models.User.objects.filter(username=line[0]).count():
                        errors.append("Line %d: Username '%s' is already taken" %
                                      (line_num, line[0]))
                        continue

                    hospital_pk = -1
                    doctor_pk = -1
                    d_errors = []
                    h_errors = []

                    if(Doctor.objects.filter(username=line[7]).count()):
                        doctor_pk = Doctor.objects.get(username=line[7]).pk
                    else:
                        errors.append("Line %d: No doctor with username '%s'" %
                                      (line_num, line[7]))

                        # Placeholder to throw form validation error
                        d_errors = ['placeholder']

                    if(Hospital.objects.filter(name=line[8]).count()):
                        hospital_pk = Hospital.objects.get(name=line[8]).pk
                    else:
                        errors.append("Line %d: No hospital named '%s'" %
                                      (line_num, line[8]))

                        # Placeholder to throw form validation error
                        h_errors = ['placeholder']

                    data = {'email': line[0], 'password': line[1], 'first_name':
                            line[2], 'last_name': line[3], 'insurance_num': line[4],
                            'birthdate': line[5], 'sex': line[6], 'dr': doctor_pk,
                            'hospital': hospital_pk}

                    f = PatientForm(user=self, data=data)
                    if d_errors:
                        f.errors['doctor'] = d_errors
                    if h_errors:
                        f.errors['hospital'] = h_errors

                    if f.is_valid():

                        patient = f.save()

                        # Generate a log event
                        event = ChangelogEntry(
                            hospital=patient.hospital,
                            time=datetime.now(),
                            generatedby=self,
                            description='Patient %s Added' % patient.__str__()
                        )
                        event.save()

                        # Now add in the optional information

                        if line[9]:
                            patient.phone = line[9]
                        if line[10]:
                            patient.address = line[10]
                        if line[11]:
                            patient.e_first_name = line[11]
                        if line[12]:
                            patient.e_last_name = line[12]
                        if line[13]:
                            patient.e_phone = line[13]

                        patient.save()

                except:
                    errors.append(["CSV file is invalid"])
                    break

        return errors

    def write_patients_to_csv(self, filename):
        """
        Write patients to a comma-separated value file
        :param filename: The filename to write to
        """

        import csv
        csv.register_dialect('escaped', delimiter=",", escapechar="\\",
                             quoting = csv.QUOTE_NONE)

        with open(filename, 'w', newline='') as csvfile:
            pat_writer = csv.writer(csvfile, dialect='escaped')

            for patient in self.hospital.patients_list.all():
                write_row = []

                # Build the list of fields
                write_row.append(patient.username)
                # We can't access the password, so make a new one
                write_row.append(u_models.User.objects.make_random_password())
                write_row.append(patient.first_name)
                write_row.append(patient.last_name)
                write_row.append(patient.insurance_num)
                write_row.append(patient.birthdate)
                write_row.append(patient.sex)
                write_row.append(patient.dr.username)
                write_row.append(patient.hospital.name)
                write_row.append(patient.phone)
                write_row.append(patient.address)
                write_row.append(patient.e_first_name)
                write_row.append(patient.e_last_name)
                write_row.append(patient.e_phone)

                # And write it to the file
                pat_writer.writerow(write_row)

    def add_doctors_from_csv(self, filename):
        """
        Add doctors from a comma-separated value file
        :param filename: The filename containing csv data
        :return: A list of errors in the upload
        """

        from .forms import DoctorForm
        import csv

        csv.register_dialect('escaped', delimiter=",", escapechar="\\")

        line_num = 0
        errors = []

        with open(filename, newline='') as csvfile:
            dr_reader = csv.reader(csvfile, dialect='escaped')
            for line in dr_reader:

                try:

                    line_num += 1

                    if not line:
                        continue

                    if u_models.User.objects.filter(username=line[0]).count():
                        errors.append("Line %d: Username '%s' is already taken" %
                                      (line_num, line[0]))
                        continue

                    hospital_pk = -1
                    h_errors = []
                    hospital_list = []

                    for hosp_name in line[6:]:
                        if(Hospital.objects.filter(name=hosp_name).count()):
                            hospital_pk = Hospital.objects.get(name=hosp_name).pk
                            hospital_list.append(hospital_pk)
                        else:
                            errors.append("Line %d: No hospital named '%s'" %
                                          (line_num, hosp_name))

                    data = {'email': line[0], 'password': line[1], 'first_name':
                            line[2], 'last_name': line[3], 'phone': line[5],
                            'hospitals_list': hospital_list}

                    f = DoctorForm(user=self, data=data)

                    if h_errors:
                        f.errors['hospital'] = h_errors

                    if f.is_valid():

                        doctor = f.save()

                        # Generate a log event
                        event = ChangelogEntry(
                            hospital=self.hospital,
                            time=datetime.now(),
                            generatedby=self,
                            description='Doctor %s Added' % doctor.__str__()
                        )
                        event.save()

                        # Now add in the optional information

                        if line[4]:
                            doctor.max_num_patients = line[4]

                        doctor.is_active = True
                        doctor.hospitals_list = hospital_list
                        doctor.save()

                except:
                    errors.append(["CSV file is invalid"])
                    break

        return errors

    def write_doctors_to_csv(self, filename):
        """
        Write doctors to a comma-separated value file
        :param filename: The filename to write to
        """

        import csv
        csv.register_dialect('escaped', delimiter=",", escapechar="\\",
                             quoting = csv.QUOTE_NONE)

        with open(filename, 'w', newline='') as csvfile:
            dr_writer = csv.writer(csvfile, dialect='escaped')

            for doctor in self.hospital.doctors_list.all():
                write_row = []

                # Build the list of fields
                write_row.append(doctor.username)
                # We can't access the password, so make a new one
                write_row.append(u_models.User.objects.make_random_password())
                write_row.append(doctor.first_name)
                write_row.append(doctor.last_name)
                write_row.append(doctor.max_num_patients)
                write_row.append(doctor.phone)

                for hospital in doctor.hospitals_list.all():
                    write_row.append(hospital)

                # And write it to the file
                dr_writer.writerow(write_row)

    def add_nurses_from_csv(self, filename):
        """
        Add nurses from a comma-separated value file
        :param filename: The filename containing csv data
        :return: A list of errors in the upload
        """

        from .forms import NurseForm
        import csv

        errors = []
        line_num = 0

        csv.register_dialect('escaped', delimiter=",", escapechar="\\")

        with open(filename, newline='') as csvfile:
            nurse_reader = csv.reader(csvfile, dialect='escaped')
            for line in nurse_reader:

                try:

                    line_num += 1

                    if not line:
                        continue

                    if u_models.User.objects.filter(username=line[0]).count():
                        errors.append("Line %d: Username '%s' is already taken" %
                                      (line_num, line[0]))
                        continue

                    dr_pk = -1
                    dr_errors = []
                    dr_list = []

                    hosp_pk = -1
                    hospital_errors = []

                    for dr_name in line[6:]:
                        if(Doctor.objects.filter(username=dr_name).count()):
                            dr_pk = Doctor.objects.get(username=dr_name).pk
                            dr_list.append(dr_pk)
                        else:
                            if dr_name:
                                errors.append("Line %d: No doctor with username '%s'" %
                                              (line_num, dr_name))
                                dr_errors.append("No doctor %s" % dr_name)

                    if Hospital.objects.filter(name=line[5]).count():
                        hosp_pk = Hospital.objects.get(name=line[5]).pk
                    else:
                        errors.append("Line %d: No hospital named '%s'" %
                                      (line_num, line[5]))
                        hospital_errors.append("No hospital %s" % line[5])

                    data = {'email': line[0], 'password': line[1], 'first_name':
                            line[2], 'last_name': line[3], 'phone': line[4],
                            'hospital': hosp_pk}

                    f = NurseForm(user=self, data=data)

                    if(hospital_errors):
                        f.errors['hospital'] = hospital_errors

                    if f.is_valid():

                        nurse = f.save()

                        # Generate a log event
                        event = ChangelogEntry(
                            hospital=nurse.hospital,
                            time=datetime.now(),
                            generatedby=self,
                            description='Nurse %s Added' % nurse.__str__()
                        )
                        event.save()

                        # Now add in the optional information

                        nurse.is_active = True
                        nurse.doctors_list = dr_list
                        nurse.save()

                except:
                    errors.append(["CSV file is invalid"])
                    break

        return errors

    def write_nurses_to_csv(self, filename):
        """
        Write nurses to a comma-separated value file
        :param filename: The filename to write to
        """

        import csv
        csv.register_dialect('escaped', delimiter=",", escapechar="\\",
                             quoting = csv.QUOTE_NONE)

        with open(filename, 'w', newline='') as csvfile:
            nurse_writer = csv.writer(csvfile, dialect='escaped')

            for nurse in self.hospital.nurses_list.all():
                write_row = []

                # Build the list of fields
                write_row.append(nurse.username)
                # We can't access the password, so make a new one
                write_row.append(u_models.User.objects.make_random_password())
                write_row.append(nurse.first_name)
                write_row.append(nurse.last_name)
                write_row.append(nurse.hospital.name)
                write_row.append(nurse.phone)

                for doctor in nurse.doctors_list.all():
                    write_row.append(doctor.username)

                # And write it to the file
                nurse_writer.writerow(write_row)

def is_doctor(user):
    """
    Takes a User object and checks if it is an instance of Doctor
    :param user: the user to check
    :return: True if it is an instance, false otherwise
    """
    return Doctor.objects.filter(pk=user.pk).count() == 1


def is_nurse(user):
    """
    Takes a User object and checks if it is an instance of Nurse
    :param user: the user to check
    :return: True if it is an instance, false otherwise
    """
    return Nurse.objects.filter(pk=user.pk).count() == 1


def is_patient(user):
    """
    Takes a User object and checks if it is an instance of Patient
    :param user: the user to check
    :return: True if it is an instance, false otherwise
    """
    return Patient.objects.filter(pk=user.pk).count() == 1


def is_admin(user):
    """
    Takes a User object and checks if it is an instance of HospitalAdmin
    :param user: the user to check
    :return: True if it is an instance, false otherwise
    """
    return HospitalAdmin.objects.filter(pk=user.pk).count() == 1


def get_user_inst(user):
    """
    Takes a User object (taken from a 'request' or call to 'authenticate()'
    and fetches the appropriate class instance from the database.

    :param user: The user to retrieve
    :return: The specific class instance of that user, or None if no user exists
    """

    if user is None:
        return False
    if user.id is None:
        return False

    uname = user.username
    upk = user.pk

    if is_doctor(user):
        return Doctor.objects.get(username=uname)
    elif is_nurse(user):
        return Nurse.objects.get(username=uname)
    elif is_patient(user):
        return Patient.objects.get(username=uname)
    elif is_admin(user):
        return HospitalAdmin.objects.get(username=uname)
    else:
        return None


class ChangelogEntry(models.Model):
    """
    Holds entries for the hospital admin's changelog
    """

    class Meta:
        verbose_name = "Admin Changelog Entry"
        verbose_name_plural = "Admin Changelog Entries"

    # Hospital this event was generated in
    hospital = models.ForeignKey('Hospital', Hospital, default=None)

    # Date this event was generated
    time = models.DateTimeField('Date Generated', default=None)

    # Who generated this event
    generatedby = models.ForeignKey(u_models.User,
                                    verbose_name="Generated By",
                                    default=None)

    # Brief description of this event
    description = models.CharField('Description', max_length=100)

    def __str__(self):
        """
        :return: A string representation of entry (its description)
        """
        return self.description


def add_emr_from_csv(filename):
    """
    Add records from a comma-separated value file
    (anonymous for command-line use)
    :param filename: The filename containing csv data
    :return: A list of errors in the upload
    """

    from emr.models import Vitals, Prescription, Test, Note
    from healthnet.models import Notification
    import csv

    errors = []
    line_num = 0

    csv.register_dialect('escaped', delimiter=",", escapechar="\\")

    with open(filename, newline='') as csvfile:
        pat_reader = csv.reader(csvfile, dialect='escaped')
        for line in pat_reader:

            try:

                line_num += 1

                if not line:
                    continue

                if not Patient.objects.filter(username=line[1]):
                    errors.append("Line %d: invalid username '%s'" %
                                  (line_num, line[1]))
                    continue

                if line[0] == "Vital":
                    patient = Patient.objects.get(username=line[1])
                    emr = patient.emr

                    height = float(line[2])
                    weight = float(line[3])
                    blood_pressure = line[4]
                    heart_rate = float(line[5])
                    cholesterol = float(line[6])

                    record = Vitals(emr=emr, height=height, weight=weight,
                                    heart_rate=heart_rate,
                                    cholesterol=cholesterol,
                                    blood_pressure_str=blood_pressure,
                                    is_released_to_patient=True,
                                    date_time=datetime.now())

                    record.save()

                elif line[0] == "Prescription":

                    patient = Patient.objects.get(username=line[1])
                    emr = patient.emr

                    name = line[2]
                    quantity = line[3]
                    dosage = line[4]
                    units = line[5]

                    record = Prescription(emr=emr, name=name, quantity=quantity,
                                          dosage=dosage, units=units,
                                          is_released_to_patient=True,
                                          date_time=datetime.now())

                    record.save()

                elif line[0] == "Test":

                    patient = Patient.objects.get(username=line[1])
                    emr = patient.emr

                    description = line[2]
                    result = line[3]
                    comments = line[4]

                    if 'f' in line[5].lower():
                        released = False
                    else:
                        released = True

                    record = Test(emr=emr, description=description,
                                  result=result, comments=comments,
                                  is_released_to_patient=released,
                                  date_time=datetime.now())

                    record.save()

                    if not record.is_released_to_patient:
                        notification = Notification(
                            receiver=patient.dr,
                            message='Test awaiting approval for patient: %s' % (
                                patient.__str__()
                            ),
                            related_action='/'
                        )
                        notification.save()

                    if line[6]:

                        try:

                            # Try to open it, to make sure it's there
                            with open(line[6]) as test:
                                pass

                            record.image.name = line[6]
                            record.save()

                        except:
                            errors.append(' '.join(
                                ["Line %d: the specified image" % (line_num),
                                 " does not exist or has moved.",
                                 " Test has been saved with no image."]))

                else:
                    errors.append("Line %d: invalid identifier '%s'",
                                  (line_num, line[0]))
            except:
                errors.append(["CSV file is invalid"])
                break

    return errors


def add_patients_from_csv(filename):
    """
    Add patients from a comma-separated value file
    (anonymous for command-line use)
    :param filename: The filename containing csv data
    :return: A list of errors in the upload
    """

    from .forms import PatientForm
    import csv

    csv.register_dialect('escaped', delimiter=",", escapechar="\\")
    errors = []

    with open(filename, newline='') as csvfile:
        pat_reader = csv.reader(csvfile, dialect='escaped')
        line_num = 0

        for line in pat_reader:

            try:

                line_num += 1

                if not line:
                    continue

                if u_models.User.objects.filter(username=line[0]).count():
                    errors.append("Line %d: Username '%s' is already taken" %
                                  (line_num, line[0]))
                    continue

                hospital_pk = -1
                doctor_pk = -1
                d_errors = []
                h_errors = []

                if (Doctor.objects.filter(username=line[7]).count()):
                    doctor_pk = Doctor.objects.get(username=line[7]).pk
                else:
                    errors.append("Line %d: No doctor with username '%s'" %
                                  (line_num, line[7]))

                    # Placeholder to throw form validation error
                    d_errors = ['placeholder']

                if (Hospital.objects.filter(name=line[8]).count()):
                    hospital_pk = Hospital.objects.get(name=line[8]).pk
                else:
                    errors.append("Line %d: No hospital named '%s'" %
                                  (line_num, line[8]))

                    # Placeholder to throw form validation error
                    h_errors = ['placeholder']

                data = {'email': line[0], 'password': line[1], 'first_name':
                    line[2], 'last_name': line[3], 'insurance_num': line[4],
                        'birthdate': line[5], 'sex': line[6], 'dr': doctor_pk,
                        'hospital': hospital_pk}

                f = PatientForm(user=None, data=data)
                if d_errors:
                    f.errors['doctor'] = d_errors
                if h_errors:
                    f.errors['hospital'] = h_errors

                if f.is_valid():

                    patient = f.save()

                    # Now add in the optional information

                    if line[9]:
                        patient.phone = line[9]
                    if line[10]:
                        patient.address = line[10]
                    if line[11]:
                        patient.e_first_name = line[11]
                    if line[12]:
                        patient.e_last_name = line[12]
                    if line[13]:
                        patient.e_phone = line[13]

                    patient.save()

            except:
                errors.append(["CSV file is invalid"])
                break

    return errors


def add_doctors_from_csv(filename):
    """
    Add doctors from a comma-separated value file
    (anonymous for command-line use)
    :param filename: The filename containing csv data
    :return: A list of errors in the upload
    """

    from .forms import DoctorForm
    import csv

    csv.register_dialect('escaped', delimiter=",", escapechar="\\")

    line_num = 0
    errors = []

    with open(filename, newline='') as csvfile:
        dr_reader = csv.reader(csvfile, dialect='escaped')
        for line in dr_reader:

            try:

                line_num += 1

                if not line:
                    continue

                if u_models.User.objects.filter(username=line[0]).count():
                    errors.append("Line %d: Username '%s' is already taken" %
                                  (line_num, line[0]))
                    continue

                hospital_pk = -1
                h_errors = []
                hospital_list = []

                for hosp_name in line[6:]:
                    if (Hospital.objects.filter(name=hosp_name).count()):
                        hospital_pk = Hospital.objects.get(name=hosp_name).pk
                        hospital_list.append(hospital_pk)
                    else:
                        errors.append("Line %d: No hospital named '%s'" %
                                      (line_num, hosp_name))

                data = {'email': line[0], 'password': line[1], 'first_name':
                    line[2], 'last_name': line[3], 'phone': line[5],
                        'hospitals_list': hospital_list}

                f = DoctorForm(user=None, data=data)

                if (h_errors):
                    f.errors['hospital'] = h_errors

                if f.is_valid():

                    doctor = f.save()
                    # Now add in the optional information

                    if line[4]:
                        doctor.max_num_patients = line[4]

                    doctor.hospitals_list = hospital_list
                    doctor.is_active = True
                    doctor.save()

            except:
                errors.append(["CSV file is invalid"])
                break

    return errors


def add_nurses_from_csv(filename):
    """
    Add nurses from a comma-separated value file
    (anonymous for command-line use)
    :param filename: The filename containing csv data
    :return: A list of errors in the upload
    """

    from .forms import NurseForm
    import csv

    errors = []
    line_num = 0

    csv.register_dialect('escaped', delimiter=",", escapechar="\\")

    with open(filename, newline='') as csvfile:
        nurse_reader = csv.reader(csvfile, dialect='escaped')
        for line in nurse_reader:

            try:

                line_num += 1

                if not line:
                    continue

                if u_models.User.objects.filter(username=line[0]).count():
                    errors.append("Line %d: Username '%s' is already taken" %
                                  (line_num, line[0]))
                    continue

                dr_pk = -1
                dr_errors = []
                dr_list = []

                hosp_pk = -1
                hospital_errors = []

                for dr_name in line[6:]:
                    if (Doctor.objects.filter(username=dr_name).count()):
                        dr_pk = Doctor.objects.get(username=dr_name).pk
                        dr_list.append(dr_pk)
                    else:
                        if dr_name:
                            errors.append("Line %d: No doctor with username '%s'" %
                                          (line_num, dr_name))
                            dr_errors.append("No doctor %s" % dr_name)

                if Hospital.objects.filter(name=line[5]).count():
                    hosp_pk = Hospital.objects.get(name=line[5]).pk
                else:
                    errors.append("Line %d: No hospital named '%s'" %
                                  (line_num, line[5]))
                    hospital_errors.append("No hospital %s" % line[5])

                data = {'email': line[0], 'password': line[1], 'first_name':
                    line[2], 'last_name': line[3], 'phone': line[4],
                        'hospital': hosp_pk}

                f = NurseForm(user=None, data=data)

                if (hospital_errors):
                    f.errors['hospital'] = hospital_errors

                if f.is_valid():
                    nurse = f.save()

                    # Now add in the optional information
                    nurse.doctors_list = dr_list
                    nurse.is_active = True
                    nurse.save()

            except:
                errors.append(["CSV file is invalid"])
                break

    return errors
