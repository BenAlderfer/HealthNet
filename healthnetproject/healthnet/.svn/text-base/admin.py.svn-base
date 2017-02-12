from django.contrib import admin
from .models import *
from django.contrib.admin import AdminSite
from django.forms import Textarea
from emr.models import *
from users.models import *


#
#
# class NotificationAdmin(admin.ModelAdmin):
#     fields = ['description', 'due_date', 'status']
#     list_display = ('description', 'due_date', 'status')
#     list_filter = ['due_date']
#     search_fields = ['description']
#
# admin.site.register(Notification, NotificationAdmin)
#
#

class AppointmentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['date_time', 'duration', 'hospital', 'note']
        }),
        ('People Involved', {
            'fields': ['patient', 'doctor']
        })
    ]

    # make a larger textbox for notes
    formfield_overrides = {
        models.TextField: {
            'widget': Textarea( attrs = { 'rows': 6, 'cols': 40 } ) },
    }

    list_display = ['doctor', 'patient', 'hospital', 'date_time']
    list_filter = ('hospital__name', 'date_time')
    search_fields = ['patient__last_name', 'patient__first_name',
                     'doctor__last_name', 'doctor__first_name',
                     'hospital__name', 'note']

admin.site.register(Appointment, AppointmentAdmin)

# Change the headers
AdminSite.site_header = 'HealthNet Management'
AdminSite.site_title = 'HealthNet Admin'
AdminSite.index_title = 'Welcome to HealthNet'