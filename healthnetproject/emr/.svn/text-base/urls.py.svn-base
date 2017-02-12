from django.conf.urls import url
from . import views

app_name = 'emr'
urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.emr, name="emr"),
    url(r'^prescriptions/(?P<pk>[0-9]+)/$', views.prescriptions, name="prescriptions"),
    url(r'^tests/(?P<pk>[0-9]+)/$', views.tests, name='tests'),
    url(r'^notes/(?P<pk>[0-9]+)/$', views.notes, name='notes'),
    url(r'^vitals/(?P<pk>[0-9]+)/$', views.vitals, name='vitals'),
    url(r'^new_vital/(?P<pk>[0-9]+)/?', views.new_vital, name='new_vital'),
    url(r'^new_test/(?P<pk>[0-9]+)/?', views.new_test, name='new_test'),
    url(r'^new_note/(?P<pk>[0-9]+)/?', views.new_note, name='new_note'),
    url(r'^new_prescription/(?P<pk>[0-9]+)/?', views.new_prescription, name='new_prescription'),
    url(r'^add_admission/(?P<pk>[0-9]+)/?', views.add_admission, name='add_admission'),
    url(r'^test_image/(?P<pk>[0-9]+)/?', views.test_image, name='test_image'),
    url(r'^edit_vital/(?P<pk>[0-9]+)/?', views.edit_vital, name='edit_vital'),
    url(r'^edit_test/(?P<pk>[0-9]+)/?', views.edit_test, name='edit_test'),
    url(r'^edit_note/(?P<pk>[0-9]+)/?', views.edit_note, name='edit_note'),
    url(r'^edit_prescription/(?P<pk>[0-9]+)/?', views.edit_prescription, name='edit_prescription'),
    url(r'^add_discharge/(?P<pk>[0-9]+)/?', views.add_discharge, name='add_discharge'),
    url(r'^add_transfer/(?P<pk>[0-9]+)/?', views.add_transfer, name='add_transfer'),
    url(r'^delete_item/(?P<pk>[0-9]+)/?', views.delete_item, name='delete_item'),
    url(r'^confirm_transfer/(?P<pk>[0-9]+)/?', views.confirm_transfer, name='confirm_transfer'),
]
