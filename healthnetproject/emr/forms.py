from django import forms
from emr.models import *

class VitalsRegForm(forms.ModelForm):
    """
    A form for entering in a patient's vitals during registration.
    """
    class Meta:
        """
        Fields and types for the form.
        """
        model = Vitals
        height = forms.DecimalField
        weight = forms.DecimalField
        blood_pressure_str = forms.CharField
        cholesterol = forms.DecimalField
        heart_rate = forms.IntegerField
        fields = ['height', 'weight', 'blood_pressure_str', 'cholesterol',
                  'heart_rate']

    def __init__(self, user, *args, **kwargs):
        super(VitalsRegForm, self).__init__(*args, **kwargs)


class VitalsEntryForm(forms.ModelForm):
    """
    A form for entering in a patient's vitals.
    """
    class Meta:
        """
        Fields and types for the form.
        """
        model = Vitals
        height = forms.DecimalField
        weight = forms.DecimalField
        blood_pressure_str = forms.CharField
        cholesterol = forms.DecimalField
        heart_rate = forms.IntegerField
        fields = ['height', 'weight', 'blood_pressure_str', 'cholesterol',
                  'heart_rate', 'is_released_to_patient']

    def __init__(self, user, patientpk, *args, **kwargs):
        self.creator = user
        self.patient = Patient.objects.get(pk=patientpk)
        super(VitalsEntryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Save function to register the form as an object
        """
        vitals = super(VitalsEntryForm, self).save(commit=False)
        vitals.height = self.cleaned_data["height"]
        vitals.weight = self.cleaned_data["weight"]
        vitals.blood_pressure_str = self.cleaned_data["blood_pressure_str"]
        vitals.cholesterol = self.cleaned_data["cholesterol"]
        vitals.heart_rate = self.cleaned_data["heart_rate"]
        vitals.emr = self.patient.emr


        # created by a doctor or nurse
        if is_doctor(self.creator):
            vitals.created_by = self.creator
            vitals.is_released_to_patient = self.cleaned_data["is_released_to_patient"]
        elif is_nurse(self.creator):
            vitals.created_by=self.creator
            vitals.is_released_to_patient = False
        else:
            # some text that will break it and throw the error page
            vitals.created_by = "no_creator_error"

        if commit:
            vitals.save()

        return vitals


class TestEntryForm(forms.ModelForm):
    """
    A form for entering in a patient's test results.
    """

    class Meta:
        model = Test
        description = forms.CharField
        result = forms.CharField
        comments = forms.CharField
        image = forms.FileField
        is_released_to_patient = forms.BooleanField
        fields = ['description', 'result', 'comments', 'is_released_to_patient', 'image']

    def __init__(self, user, patientpk, *args, **kwargs):
        self.creator = user
        self.patient = Patient.objects.get(pk=patientpk)
        super(TestEntryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        test = super(TestEntryForm, self).save(commit=False)
        test.description = self.cleaned_data['description']
        test.result = self.cleaned_data['result']
        test.comments = self.cleaned_data['comments']
        test.image = self.cleaned_data['image']
        # created by doctor
        if is_doctor(self.creator):
            # doctor decides to release to patient
            test.is_released_to_patient = \
                self.cleaned_data['is_released_to_patient']
            test.created_by = self.creator
        # created by nurse
        elif is_nurse(self.creator):
            # nurse cannot release to patient
            test.is_released_to_patient = False
            test.created_by = self.creator
        else:
            # random text that will break it and throw error page
            test.created_by = "no_creator_error"
        test.emr = self.patient.emr

        if commit:
            test.save()

        return test


class NotesEntryForm(forms.ModelForm):
    """
    A form for adding a note to a patient EMR.
    """

    class Meta:
        model = Note
        message = forms.CharField
        is_released_to_patient = forms.BooleanField
        fields = ['message', 'is_released_to_patient']

    def __init__(self, user, patientpk, *args, **kwargs):
        self.creator = user
        self.patient = Patient.objects.get(pk=patientpk)
        super(NotesEntryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        note = super(NotesEntryForm, self).save(commit=False)
        note.message = self.cleaned_data['message']
        note.emr = self.patient.emr
        if is_doctor(self.creator):
            # doctor decides to release to patient
            note.is_released_to_patient = \
                self.cleaned_data['is_released_to_patient']
            note.created_by = self.creator
        # created by nurse
        elif is_nurse(self.creator):
            # nurse cannot release to patient
            note.is_released_to_patient = False
            note.created_by = self.creator
        else:
            # random text that will break it and throw error page
            note.created_by = "no_creator_error"
        note.emr = self.patient.emr
        if commit:
            note.save()

        return note


class PrescriptionEntryForm(forms.ModelForm):
    """
    A form for adding a prescription to an EMR.
    """

    class Meta:
        model = Prescription
        name = forms.CharField
        quantity = forms.IntegerField
        units = forms.CharField
        is_released_to_patient = forms.BooleanField
        fields = ['name', 'quantity', 'units', 'dosage']

    def __init__(self, user, patientpk, *args, **kwargs):
        self.creator = user
        self.patient = Patient.objects.get(pk=patientpk)
        super(PrescriptionEntryForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        prescription = super(PrescriptionEntryForm, self).save(commit=False)
        prescription.created_by = self.creator
        prescription.name = self.cleaned_data['name']
        prescription.dosage= self.cleaned_data['dosage']
        prescription.quantity = self.cleaned_data['quantity']
        prescription.units = self.cleaned_data['units']

        prescription.is_released_to_patient = True

        prescription.emr = self.patient.emr

        if commit:
            prescription.save()

        return prescription


class AdmissionForm(forms.ModelForm):
    """
    A form for adding an Admisison to a patient.
    """

    def __init__(self, user, *args, **kwargs):
        super(AdmissionForm, self).__init__(*args, **kwargs)
        self.fields['hospital'] = forms.ModelChoiceField(
            queryset=Hospital.objects.all()
        )
        self.fields['doctor'] = forms.ModelChoiceField(
            queryset=Doctor.objects.all()
        )
        self.user = user

    class Meta:
        model = Admission
        reason = forms.CharField()
        doctor = forms.ChoiceField()
        hospital = forms.ChoiceField()
        fields = ['hospital', 'doctor', 'reason']

    def save(self, commit=True):
        admission = super(AdmissionForm, self).save(commit=False)
        admission.doctor = self.cleaned_data['doctor']
        admission.hospital = self.cleaned_data['hospital']
        admission.created_by = get_user_inst(self.user)

        return admission


class TransferForm(forms.ModelForm):
    """
    A form for adding a Transfer to a patient
    """
    def __init__(self, user, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['receiving_hospital'] = forms.ModelChoiceField(
            queryset=Hospital.objects.all()
        )
        self.fields['receiving_doctor'] = forms.ModelChoiceField(
            queryset=Doctor.objects.all()
        )
        self.user = user

    class Meta:
        model = Transfer
        receiving_hospital = forms.ChoiceField()
        receiving_doctor = forms.ChoiceField()
        reason = forms.CharField()
        fields = ['receiving_hospital', 'receiving_doctor', 'reason']

    def save(self, commit=True):
        transfer = super(TransferForm, self).save(commit=False)
        if is_admin(self.user):
            transfer.receiving_doctor = self.cleaned_data['receiving_doctor']
            transfer.receiving_hospital = \
                self.cleaned_data['receiving_hospital']
        transfer.created_by = get_user_inst(self.user)
        transfer.reason = self.cleaned_data['reason']

        return transfer
