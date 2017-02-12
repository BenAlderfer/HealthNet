from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite
from django.forms import Textarea

# Register your models here.


class ChangelogAdmin(admin.ModelAdmin):
    readonly_fields = ['time', 'hospital', 'generatedby', 'description']
    fields = ['time', 'hospital', 'generatedby', 'description']
    list_display = ('time', 'hospital', 'generatedby', 'description')
    list_filter = ('time', 'hospital')
    search_fields = ['hospital', 'generatedby', 'description']

admin.site.register(ChangelogEntry, ChangelogAdmin)


class HospitalAdminAdmin(admin.ModelAdmin):
    """
    A class for viewing the appropriate attributes of the HospitalAdmin model in
         the admin page.

    Fields to include: last name, first name, hospital, username, password
    """
    fields = [('first_name', 'last_name'), 'username',
              'phone', 'hospital', 'is_active']
    list_display = ('last_name', 'first_name', 'hospital', 'is_active')
    list_filter = ('hospital__name', 'is_active')
    search_fields = ['last_name']

admin.site.register(HospitalAdmin, HospitalAdminAdmin)


class HospitalBuildingAdmin(admin.ModelAdmin):
    """
     A class for viewing the appropriate attributes of the Hospital model in
         the admin page.

     Fields to include: name, number of patients, maximum number of patients
    """
    # can be seen but not edited
    readonly_fields = ('get_num_patients',)
    # visible in individual editing page
    fieldsets = [
        # hospital name
        (None,  {'fields': ['name']}),

        # patient capacity section with current and max number of patients
        ('Patient Capacity',  {
            'fields': ['get_num_patients', 'max_num_patients']
        }),
    ]
    # shown in list display
    list_display = ('name', 'get_num_patients', 'max_num_patients')
    # can be searched by
    search_fields = ['name']

admin.site.register(Hospital, HospitalBuildingAdmin)


class DoctorAdmin(admin.ModelAdmin):
    """
     A class for viewing the appropriate attributes of the Doctor model in
         the admin page.

     Fields to include: last name, first name, hospital, number of patients,
        maximum number of patients, list of patients, username, password
    """
    # cannot be changed
    readonly_fields = ['get_num_patients', 'patient_list']
    # displayed and editable
    fieldsets = [
        (None, {'fields': [('first_name', 'last_name'), 'hospitals_list',
                           'username', 'phone', 'is_active']}),
        ('Patient Capacity', {
            'fields': ['get_num_patients', 'max_num_patients', 'patient_list']
        })
    ]
    # displayed in list
    list_display = ('last_name', 'first_name', 'at_max_patients',
                    'is_active')
    # can be filtered by
    list_filter = ('hospitals_list', 'is_active')
    # can be searched
    search_fields = ['last_name']

admin.site.register(Doctor, DoctorAdmin)


class PatientAdmin(admin.ModelAdmin):
    """
     A class for viewing the appropriate attributes of the Patient model in
        the admin page.

     Fields to include: last name, first name, gender, sex, birthdate,
        insurance number, hospital, doctor, username, password, phone number
    """

    fieldsets = [
        (None, {
            'fields': [('first_name', 'last_name'), ('gender', 'sex'),
                       'birthdate', 'phone']}),
        ('Login Information', {
            'fields': ['username',]
        }),
        ('Medical Information', {
            'fields': ['insurance_num', 'hospital', 'dr']
        })
    ]
    list_display = ('last_name', 'first_name', 'insurance_num', 'hospital',
                    'dr', 'is_active')
    list_filter = ('hospital__name', )
    search_fields = ['last_name']

admin.site.register(Patient, PatientAdmin)


class NurseAdmin(admin.ModelAdmin):
    """
    A class for viewing the appropriate attributes of the Nurse model in
         the admin page.

    Fields to include: last name, first name, hospital, patient list,
        doctor list, username, password
    """
    readonly_fields = ['patients_list', ]
    fieldsets = [
        (None, {
            'fields': [('first_name', 'last_name'), 'hospital',
                       'username', 'phone', 'is_active']
        }),
        ('Related Users', {
            'fields': ['doctors_list', 'patients_list']
        })
    ]
    list_display = ('last_name', 'first_name', 'hospital', 'is_active')
    list_filter = ['hospital__name']
    search_fields = ['last_name']

admin.site.register(Nurse, NurseAdmin)
