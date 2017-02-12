from django.contrib import admin
from .models import *

# Register your models here.


class EMRAdmin(admin.ModelAdmin):
    """
    A class for viewing EMR models through the admin panel.
    """

    readonly_fields = ('num_items',)
    fields = ['patient', 'num_items']
    list_display = fields
    search_fields = ['patient__last_name']

admin.site.register(EMR, EMRAdmin)


class EMRItemAdmin(admin.ModelAdmin):
    """
    A class for viewing the appropriate attributes of the EMRItem model in
         the admin page.

    Fields to include: patient, creation time, creator, released to patient
    """
    readonly_fields = ['emr', 'date_time', 'creator']
    fieldsets = [
       (None, {
           'fields': ['emr', 'date_time', 'created_by',
                      'is_released_to_patient']
       }),
       # ('Patient', {
       #    'fields': ['patient']
       # })
    ]
    list_display = ('emr', 'creator', 'date_time')
    list_filter = ['date_time']
    search_fields = ['creator']

admin.site.register(EMRItem, EMRItemAdmin)


class PrescriptionAdmin(admin.ModelAdmin):
    """
    A class for viewing the appropriate attributes of the Prescription model in
       the admin page.

    Fields to include: all fields from EMRItem, name, quantity
    """

    readonly_fields = ['date_time', 'creator', 'dosage_str']
    fieldsets = [
        ('General', {
            'fields': ['emr', 'date_time', 'created_by',
                       'is_released_to_patient']
        }),
        ('Prescription Specific', {
            'fields': ['name', 'quantity', ('dosage', 'units')]
        })
    ]
    list_display = ['name', 'quantity', 'dosage_str', 'emr', 'date_time']
    list_filter = ['name']
    search_fields = ['name', 'emr']

admin.site.register(Prescription, PrescriptionAdmin)


class VitalsAdmin(admin.ModelAdmin):
    readonly_fields = ['date_time', 'created_by']
    fields = ['emr', 'date_time', 'created_by', ('height', 'weight',
                                                 'blood_pressure_str',
                                                 'cholesterol', 'heart_rate')]
    list_display = ('date_time', 'emr', 'created_by')
    list_filter = ['date_time']
    search_fields = ['emr', 'created_by']

admin.site.register(Vitals, VitalsAdmin)


class TestAdmin(admin.ModelAdmin):
    readonly_fields = ['date_time', 'created_by']
    fields = ['emr', 'date_time', 'created_by', ('description', 'result',
                                                 'comments')]
    list_display = ('date_time', 'emr', 'created_by')
    list_filter = ['date_time']
    search_fields = ['emr', 'created_by']

admin.site.register(Test, TestAdmin)


class NoteAdmin(admin.ModelAdmin):
    readonly_fields = ['date_time', 'created_by']
    fields = ['emr', 'date_time', 'created_by', 'message']
    list_display = ('date_time', 'emr', 'created_by')
    list_filter = ['date_time']
    search_fields = ['emr', 'created_by']

admin.site.register(Note, NoteAdmin)


class ChangeInStatusAdmin(admin.ModelAdmin):
    readonly_fields = ['date_time', 'created_by']
    fields = ['emr', 'date_time', 'created_by']
    list_display = ('date_time', 'emr', 'created_by')
    list_filter = ['date_time']
    search_fields = ['emr', 'created_by']

admin.site.register(ChangeInStatus, ChangeInStatusAdmin)


class AdmissionAdmin(admin.ModelAdmin):
    readonly_fields = ['date_time', 'created_by']
    fields = ['emr', 'date_time', 'created_by', 'reason', 'hospital', 'doctor']
    list_display = ('date_time', 'emr', 'hospital', 'doctor', 'reason')
    list_filter = ['date_time', 'hospital', 'reason']
    search_fields = ['emr', 'hospital', 'doctor']

admin.site.register(Admission, AdmissionAdmin)


class DischargeAdmin(admin.ModelAdmin):
    readonly_fields = ['date_time', 'created_by']
    fields = ['emr', 'date_time', 'created_by', 'hospital', 'doctor']
    list_display = ('date_time', 'emr', 'hospital', 'doctor')
    list_filter = ['date_time', 'hospital']
    search_fields = ['emr', 'hospital', 'doctor']

admin.site.register(Discharge, DischargeAdmin)


class TransferAdmin(admin.ModelAdmin):
    readonly_fields = ['date_time', 'created_by']

    fields = ['emr', 'date_time', 'created_by', ('hospital',
              'doctor'), ('receiving_hospital', 'receiving_doctor')]
    list_display = ('date_time', 'emr', 'hospital',
                    'receiving_hospital')
    list_filter = ['date_time', 'hospital', 'receiving_hospital']
    search_fields = ['hospital', 'doctor', 'receiving_hospital',
                     'receiving_doctor', 'emr']

admin.site.register(Transfer, TransferAdmin)
