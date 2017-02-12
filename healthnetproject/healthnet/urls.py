from django.conf.urls import url
from . import views

app_name = 'healthnet'
urlpatterns = [
    url(r'^stats/(?P<pk>[0-9]+)/$', views.stats, name='stats'),
    url(r'^permission_denied/$', views.denied, name='denied'),
    url(r'^add_appointment/(?P<pk>[0-9]+)/$', views.add_appointment, name='add_appointment'),
    url(r'^delete_appointment/(?P<pk>[0-9]+)/$', views.delete_appointment, name='delete_appointment'),
    url(r'^edit_appointment/(?P<pk>[0-9]+)/$', views.edit_appointment, name='edit_appointment'),
    url(r'^get_events/(?P<pk>[0-9]+)/$', views.get_events, name='get_events'),
    url(r'^h_admin/(?P<pk>[0-9]+)/$', views.admin_dashboard, name='admin_dashboard'),
    url(r'^doctor/(?P<pk>[0-9]+)/$', views.doctor_dashboard,
        name='doctor_dashboard'),
    url(r'^patient/(?P<pk>[0-9]+)/$', views.patient_dashboard,
        name='patient_dashboard'),
    url(r'^nurse/(?P<pk>[0-9]+)/$', views.nurse_dashboard,
        name='nurse_dashboard'),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^calendar/(?P<pk>[0-9]+)/$', views.calendar, name="calendar"),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^dismiss_notification/(?P<pk>[0-9]+)/', views.dismiss_notification, name='dismiss_notification'),
    url(r'^send_message/(?P<pk>[0-9]+)/', views.send_message, name='send_message')
]
