from django.db import models
import django.contrib.auth.models as u_models
from django.core.validators import *
from datetime import datetime
from healthnet.models import *
from users.models import *
from django.conf import settings


class EMR(models.Model):
    """
    A container for EMRItems that keeps its associated patient.
    """

    class Meta:
        verbose_name = "Electronic Medical Record"

    # the patient this EMR is associated with
    patient = models.OneToOneField('users.Patient', related_name='emr')

    @property
    def num_items(self):
        return self.emritems_list.count

    def __str__(self):
        last = self.patient.last_name
        first = self.patient.first_name
        return last + ', ' + first

    def latest_transfer(self):
        return Transfer.objects.filter(emr=self.patient.emr).\
            order_by('date_time').last()

    def latest_admission(self):
        return Admission.objects.filter(emr=self.patient.emr).\
            order_by('date_time').last()

    def latest_changeinstatus_is_transfer(self):
        c = ChangeInStatus.objects.filter(emr=self.patient.emr).\
            order_by('date_time').last()
        t = self.latest_transfer()
        if c is None or t is None:
            return False
        return c.date_time == t.date_time


class EMRItem(models.Model):
    """
    A superclass for all EMR items. Contains attributes common to all EMR items.
    """

    class Meta:
        verbose_name = "EMR Item"

    # attach each EMR item to the EMR
    emr = models.ForeignKey(EMR, on_delete=models.CASCADE,
                            related_name='emritems_list')

    emr.short_description = 'Related Patient'

    # the date and time the item was created
    # automatically set to "now" when instance is created
    date_time = models.DateTimeField(auto_now_add=True)
    date_time.short_description = 'Date and Time Created'

    # the user (doctor or nurse) who created the item
    created_by = models.ForeignKey(u_models.User,
                                   related_name='items_list', blank=True,
                                   null=True)

    @property
    def creator(self):
        return get_user_inst(getattr(self, 'created_by'))

    # whether the emr is released to patient
    # automatically set to not release to patient
    is_released_to_patient = models.BooleanField(default=False)


class Prescription(EMRItem):
    """
    A class for all Prescription items. Inherits from EMRItem.
    """

    class Meta:
        verbose_name = "Prescription"

    # the name of the prescription
    # maximum length is 150 characters
    name = models.CharField('Prescription name', max_length=150)

    # the quantity of the prescription (ie. number of pills)
    # no decimals, only integers allowed
    quantity = models.IntegerField('Quantity')

    # the dosage of the prescription
    dosage = models.IntegerField('Dosage', default=5)
    # the units of the dosage of the prescription
    units = models.CharField('Units of dosage', max_length=5,
                             help_text="Please use abbreviations", default='mg')

    def dosage_str(self):
        return str(getattr(self, 'dosage')) + ' ' + getattr(self, 'units')

    dosage_str.short_description = 'Dosage'


class Vitals(EMRItem):
    """
    A class for vital information about patient health.
    """

    class Meta:
        verbose_name_plural = "Vitals"

    is_released_to_patient = True

    # the height of the patient in inches
    height = models.DecimalField('Height', max_digits=3, decimal_places=1,
                                 blank=True, null=True)

    # weight of patient as given in pounds
    weight = models.DecimalField('Weight', blank=True, max_digits=4,
                                 decimal_places=1, null=True)

    # the systolic blood pressure
    # integers only
    blood_pressure_str = models.CharField('Blood Pressure', blank=True,
                                          max_length=7, null=True)

    # blood pressure as represented by a tuple containing the systolic and
    # diastolic blood pressures
    # TODO: implement a function that converts the blood_pressure_str to an
    # TODO: integer tuple

    # the cholesterol of the patient in mg/dL
    # integers only
    cholesterol = models.DecimalField('Cholesterol', decimal_places=1,
                                      max_digits=4, blank=True, null=True)

    # the heart rate of the patient in beats/min
    # integers only
    heart_rate = models.IntegerField('Heart rate', blank=True, null=True)


class Test(EMRItem):
    """
    A class for test items.
    """
    # the description of the test performed
    # maximum length of 500 characters
    description = models.CharField('Description', max_length=500, blank=False)

    # the result of the test performed
    # maximum length of 500 characters
    result = models.CharField('Result', max_length=500, blank=False)

    # any additional comments on the test
    # maximum length of 500 characters
    comments = models.CharField('Comments', max_length=500, blank=True)

    # optional image attached to test
    image = models.FileField('Optional image', blank=True, upload_to=
                               (settings.MEDIA_ROOT + '/uploads/tests'),
                             max_length=200)


class Note(EMRItem):
    """
    A class for notes on patient EMRs.
    """

    # a message to put on the patient EMR
    # maximum length of 500 characters
    message = models.CharField('Message', max_length=500)


class ChangeInStatus(EMRItem):
    """
    A superclass for admissions, discharges, transfers, and lengthening of
    current stays.
    Provides attributes common to all.
    """

    class Meta:
        verbose_name = 'Status Change'

    doctor = models.ForeignKey('users.Doctor',
                               related_name='status_change_list', null=True)
    hospital = models.ForeignKey('users.Hospital',
                                 related_name='status_change_list', null=True)

    is_released_to_patient = True


class Admission(ChangeInStatus):
    """
    A class for recording when a patient is admitted to a hospital.
    """
    REASON_CHOICES = (
        ('SUR', 'Surgery'),
        ('EMER', 'Emergency'),
        ('OBS', 'Observation'),
        ('OTH', 'Other'),
    )
    # reason for change in status
    # maximum length of 200 characters
    # some common potential choices provided
    reason = models.CharField('Reason', max_length=150, choices=REASON_CHOICES,
                              default='OTH')


class Discharge(ChangeInStatus):
    """
    A class for recording discharges of patients from hospital.
    """

    def initialize(self):
        # the initial admission of the patient
        self.to_current_status = self.emr.latest_admission()

        # most recent admission or transfer item
        self.most_recent = self.emr.latest_admission()

        # the hospital the patient is discharged from
        self.hospital = self.most_recent.hospital

        # the doctor the patient was assigned to
        self.doctor = self.most_recent.doctor


class Transfer(ChangeInStatus):
    """
    A class for recording transfers of patients.
    """

    def initialize(self, user):
        """
        a constructor to get the current user
        :param user: the currently logged in user
        """

        # most recent admission or transfer item
        self.most_recent = self.emr.latest_admission()

        # the doctor the patient is currently with
        if self.most_recent:
            self.doctor = self.most_recent.doctor
        else:
            self.doctor = None
        

        # the hospital the patient is currently at
        if self.most_recent:
            self.hospital = self.most_recent.hospital
        else:
            self.hospital = None

        if is_doctor(user):
            # if a doctor creates the transfer, it needs to be accepted
            self.is_accepted = False

        elif is_admin(user):
            # if a hospital admin creates the transfer, it does not need to be
            # accepted
            self.is_accepted = True

            # if the transfer is admin-created, the accepted datetime is auto-
            # filled
            self.date_time_accepted = models.DateTimeField(auto_now_add=True)

    # the hospital the patient is going to
    receiving_hospital = models.ForeignKey('users.Hospital',
                                           related_name='transfers_list',
                                           default=0)

    # the doctor the patient is going to
    receiving_doctor = models.ForeignKey('users.Doctor',
                                         related_name='transfers_list',
                                         default=0)

    REASON_CHOICES = (
        ('SUR', 'Surgery'),
        ('EMER', 'Emergency'),
        ('OBS', 'Observation'),
        ('OTH', 'Other'),
    )
    # reason for change in status
    # maximum length of 200 characters
    # some common potential choices provided
    reason = models.CharField('Reason', max_length=150, choices=REASON_CHOICES,
                              default='OTH')

    @property
    def accepted(self):
        return self.is_accepted

    def accept_transfer(self):
        """
        method for when receiving doctor accepts the transfer
        """
        self.is_accepted = True
        self.date_time_accepted = models.DateTimeField(auto_now=True)


