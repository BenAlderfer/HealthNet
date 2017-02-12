from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
    url(r'^profile/$', views.profile, name="profile"),
    url(r'^register_patient/$', views.patient_register,
        name='patient_register'),
    url(r'^patient_confirmed/$', views.patient_confirmed,name='patient_confirmed'),
    url(r'^register_staff/$', views.staff_register, name='staff_register'),
    url(r'^staff_confirmed/$', views.staff_confirmed,name='staff_confirmed'),
    url(r'^insurance_warning/$', views.insurance_warning,
        name='insurance_warning'),

    url(r'^upload/$', views.csv_upload, name='csv_upload'),

    url(r'^patients/$', views.patients, name='patients'),

    # Some narsty argument parsing stuff
    # Just filter by doctor
    url(r'^patients/d_(?P<doctor>[0-9]+)/$', views.patients, name='patients'),
    # Just filter by hospital
    url(r'^patients/h_(?P<hospital>[0-9]+)/$', views.patients, name='patients'),
    # Just filter by search key
    url(r'^patients/c_(?P<search>[,\w\-\x20]*)(.*)/$', views.patients, name='patients'),

    # Doctor and hospital
    url(r'^patients/d_(?P<doctor>[0-9]+)h_(?P<hospital>[0-9]+)/$',
        views.patients, name='patients'),

    # Doctor and search key
    url(r'^patients/d_(?P<doctor>[0-9]+)c_(?P<search>[,\w\-\x20]*)(.*)/$',
        views.patients, name='patients'),

    # Hospital and search key
    url(r'^patients/h_(?P<hospital>[0-9]+)c_(?P<search>[,\w\-\x20]*)(.*)/$',
        views.patients, name='patients'),

    # All three
    url(r'^patients/d_(?P<doctor>[0-9]+)h_(?P<hospital>[0-9]+)c_(?P<search>[,\w\-\x20]*)(.*)/$',
        views.patients, name='patients'),

    url(r'^manage/(?P<pk>[0-9]+)/$', views.manage, name='manage'),
    url(r'^log/(?P<pk>[0-9]+)/(?P<page>[0-9]+)/$', views.log, name='log'),
    url(r'^log/(?P<pk>[0-9]+)/$', views.log, name='log'),
]
