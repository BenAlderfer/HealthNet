from django.db import models
import django.contrib.auth.models as u_models
from django.core.validators import *
from datetime import datetime
from datetime import timedelta
from users.models import *


class Notification(models.Model):
    """
    class for a notification to be presented to a doctor, maybe nurse, or admin
    """

    # user receiving the message
    receiver = models.ForeignKey(
        u_models.User, on_delete=models.CASCADE,
        related_name='notifications_list'
    )

    # a short message regarding the notification
    message = models.CharField(max_length=200)

    # an action to be performed that would resolve the issue in the notification
    # this will be a url pointing to the page to go to
    related_action = models.CharField(max_length=200)


class Appointment(models.Model):
    """
    A class for recording an appointment by a patient with a specific
    doctor at a specific hospital
    """
    # date of appointment
    date_time = models.DateTimeField('Appointment Date')

    # patient with appointment
    patient = models.ForeignKey(
        'users.Patient', on_delete=models.CASCADE,
        related_name='appointments_list'
    )

    # doctor appointment is made with
    doctor = models.ForeignKey(
        'users.Doctor', on_delete=models.CASCADE,
        related_name='appointments_list'
    )

    # location of appointment
    hospital = models.ForeignKey(
        'users.Hospital', on_delete=models.CASCADE,
        related_name='appointments_list'
    )

    duration = models.IntegerField('Duration of appointment',
                                   help_text='in minutes',
                                   default=30)

    # doctor's note
    note = models.TextField(max_length=500)


    def get_end(self):
        """
        gets end time of appointment based on duration
        """
        return self.date_time + timedelta(minutes=self.duration)

