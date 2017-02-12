from django import forms
from .models import *
from emr.models import *


class PatientForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        """
        init function to set up choices for pull down menu fields
        """
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['hospital'] = forms.ModelChoiceField(
            queryset=Hospital.objects.all()
        )
        self.fields['dr'] = forms.ModelChoiceField(
            queryset=Doctor.objects.all()
        )

    class Meta:
        """
        fields and types for the form
        """
        model = Patient
        first_name = forms.CharField()
        last_name = forms.CharField()
        insurance_num = forms.CharField()
        email = forms.CharField()
        password = forms.CharField()
        sex = forms.ChoiceField()
        gender = forms.ChoiceField()
        hospital = forms.ChoiceField()
        dr = forms.ChoiceField()
        phone = forms.CharField()
        address = forms.CharField()
        birthdate = forms.DateField
        e_first_name = forms.CharField()
        e_last_name = forms.CharField()
        e_phone = forms.CharField()
        fields = ['first_name', 'last_name', 'insurance_num', 'email',
                  'password', 'sex', 'gender', 'hospital', 'dr', 'phone',
                  'address', 'birthdate', 'e_first_name', 'e_last_name',
                  'e_phone']

    def save(self, commit=True):
        """
        save function to register the form as an object
        """
        patient = super(PatientForm, self).save(commit=False)
        patient.first_name = self.cleaned_data["first_name"]
        patient.last_name = self.cleaned_data["last_name"]
        patient.insurance_num = self.cleaned_data["insurance_num"]
        patient.username = self.cleaned_data["email"]
        patient.email = self.cleaned_data["email"]
        patient.set_password(self.cleaned_data["password"])
        patient.sex = self.cleaned_data["sex"]
        patient.gender = self.cleaned_data["gender"]
        patient.e_first_name = self.cleaned_data["e_first_name"]
        patient.e_last_name = self.cleaned_data["e_last_name"]
        patient.e_phone = self.cleaned_data["e_phone"]

        hospital = self.cleaned_data["hospital"]
        # no objects text
        if hospital != "No Hospitals are available.":
            patient.hospital = hospital
        else:
            # just some random text that will break it and throw the error page
            patient.hospital = "no_hospital_error"

        dr = self.cleaned_data["dr"]
        if dr != "No Doctors are available.":  # no objects text
            patient.dr = dr
        else:
            # just some random text that will break it and throw the error page
            patient.dr = "no_doctor_error"

        patient.phone = self.cleaned_data["phone"]
        patient.birthdate = self.cleaned_data["birthdate"]
        patient.address = self.cleaned_data["address"]

        if commit:
            patient.save()

            # Create the EMR for this patient
            newemr = EMR()
            newemr.patient = patient
            newemr.save()

        return patient


class StaffForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()
    role = forms.ChoiceField()
    phone = forms.CharField()
    fields = ['first_name', 'last_name', 'email', 'password', 'role',
               'phone']


class DoctorForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        # self.fields['hospitals_list'] = forms.ModelMultipleChoiceField(
        #     queryset=Hospital.objects.all()
        # )

    class Meta:
        model = Doctor
        first_name = forms.CharField()
        last_name = forms.CharField()
        email = forms.CharField()
        password = forms.CharField()
        phone = forms.CharField()
        fields = ['first_name', 'last_name', 'email', 'password',
                  'hospitals_list', 'phone']

    def save(self, commit=True):
        doctor = super(DoctorForm, self).save(commit=False)
        doctor.first_name = self.cleaned_data["first_name"]
        doctor.last_name = self.cleaned_data["last_name"]
        doctor.username = self.cleaned_data["email"]
        doctor.email = self.cleaned_data["email"]
        doctor.set_password(self.cleaned_data["password"])
        doctor.phone = self.cleaned_data["phone"]

        doctor.is_active = False

        if commit:
            doctor.save()

        return doctor


class NurseForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(NurseForm, self).__init__(*args, **kwargs)
        self.fields['hospital'] = forms.ModelChoiceField(
            queryset=Hospital.objects.all()
        )

    class Meta:
        model = Nurse
        first_name = forms.CharField()
        last_name = forms.CharField()
        email = forms.CharField()
        password = forms.CharField()
        hospital = forms.ChoiceField()
        phone = forms.CharField()
        fields = ['first_name', 'last_name', 'email', 'password',
                  'hospital', 'phone']

    def save(self, commit=True):
        nurse = super(NurseForm, self).save(commit=False)
        nurse.first_name = self.cleaned_data["first_name"]
        nurse.last_name = self.cleaned_data["last_name"]
        nurse.username = self.cleaned_data["email"]
        nurse.email = self.cleaned_data["email"]
        nurse.set_password(self.cleaned_data["password"])
        nurse.phone = self.cleaned_data["phone"]

        hospital = self.cleaned_data["hospital"]
        if hospital != "No Hospitals are available.":  # no objects text
            nurse.hospital = hospital
        else:
            # just some random text that will break it and throw the error page
            nurse.hospital = "no_hospital_error"

        nurse.is_active = False

        if commit:
            nurse.save()

        return nurse


class AdminForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)
        self.fields['hospital'] = forms.ModelChoiceField(
            queryset=Hospital.objects.all()
        )

    class Meta:
        model = HospitalAdmin
        first_name = forms.CharField()
        last_name = forms.CharField()
        email = forms.CharField()
        password = forms.CharField()
        hospital = forms.ChoiceField()
        phone = forms.CharField()
        fields = ['first_name', 'last_name', 'email', 'password',
                  'hospital', 'phone']

    def save(self, commit=True):
        admin = super(AdminForm, self).save(commit=False)
        admin.first_name = self.cleaned_data["first_name"]
        admin.last_name = self.cleaned_data["last_name"]
        admin.username = self.cleaned_data["email"]
        admin.email = self.cleaned_data["email"]
        admin.set_password(self.cleaned_data["password"])
        admin.phone = self.cleaned_data["phone"]

        hospital = self.cleaned_data["hospital"]
        if hospital != "No Hospitals are available.":  # no objects text
            admin.hospital = hospital
        else:
            # just some random text that will break it and throw the error page
            admin.hospital = "no_hospital_error"

        admin.is_active = False

        if commit:
            admin.save()

        return admin

class CSVImportForm(forms.Form):

    csvfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
