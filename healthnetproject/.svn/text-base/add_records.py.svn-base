import sys, os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'healthnetsite.settings'
django.setup()

from django.conf import settings

from users.models import *

path = "doctors.csv"
try:
    file = open(path, "r")
    file.close()
    errors = add_doctors_from_csv(path)
    for error in errors:
        print(error)
except IOError:
    print("No doctor file (%s) found" % path)

path = "nurses.csv"
try:
    file = open(path, "r")
    file.close()
    errors = add_nurses_from_csv(path)
    for error in errors:
        print(error)
except IOError:
    print("No nurse file (%s) found" % path)

path = "patients.csv"
try:
    file = open(path, "r")
    file.close()
    errors = add_patients_from_csv(path)
    for error in errors:
        print(error)
except IOError:
    print("No patient file (%s) found" % path)

path = "emr.csv"
try:
    file = open(path, "r")
    file.close()
    errors = add_emr_from_csv(path)
    for error in errors:
        print(error)
except IOError:
    print("No emr file (%s) found" % path)
