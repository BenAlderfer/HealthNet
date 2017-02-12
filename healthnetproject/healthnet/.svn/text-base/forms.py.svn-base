from django import forms
from .models import *
from emr.models import *


class VitalsForm(forms.ModelForm):
    class Meta:
        model = Vitals
        height = forms.DecimalField()
        weight = forms.DecimalField()
        cholesterol = forms.DecimalField()
        heart_rate = forms.IntegerField()
        blood_pressure_str = forms.CharField()
        fields = ['height', 'weight', 'cholesterol', 'heart_rate',
                  'blood_pressure_str']


class AppointmentForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['hospital'] = forms.ModelChoiceField(
            queryset=Hospital.objects.all()
        )
        self.fields['patient'] = forms.ModelChoiceField(
            queryset=Patient.objects.all()
        )
        self.fields['doctor'] = forms.ModelChoiceField(
            queryset=Doctor.objects.all()
        )

    class Meta:
        model = Appointment
        date_time = forms.DateTimeField()
        duration = forms.IntegerField()
        hospital = forms.ChoiceField()
        note = forms.CharField()
        patient = forms.ChoiceField()
        doctor = forms.ChoiceField()
        fields = ['date_time', 'duration', 'hospital',
                  'note', 'patient', 'doctor']

    def save(self, commit=True):
        appointment = super(AppointmentForm, self).save(commit=False)
        appointment.date_time = self.cleaned_data["date_time"]
        appointment.duration = self.cleaned_data["duration"]
        appointment.note = self.cleaned_data["note"]

        hospital = self.cleaned_data["hospital"]
        if hospital != "No Hospitals are available.":  # no objects text
            appointment.hospital = hospital
        else:
            # just some random text that will break it and throw the error page
            appointment.hospital = "no_hospital_error"

        patient = self.cleaned_data["patient"]
        if patient != "No Patients are available.":  # no objects text
            appointment.patient = patient
        else:
            # just some random text that will break it and throw the error page
            appointment.patient = "no_patient_error"

        doctor = self.cleaned_data["doctor"]
        if doctor != "No Doctors are available.":  # no objects text
            appointment.doctor = doctor
        else:
            # just some random text that will break it and throw the error page
            appointment.doctor = "no_doctor_error"

        if commit:
            appointment.save()

        return appointment


