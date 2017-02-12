import sys, os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'healthnetsite.settings'
django.setup()

from django.conf import settings

from users.models import *

path = input("Input doctor file name: ")
try:
    file = open(path, "r")
    file.close()
    errors = add_doctors_from_csv(path)
    for error in errors:
        print(error)
except IOError:
    print("No doctor file (%s) found" % path)

path = input("\nInput nurse file name: ")
try:
    file = open(path, "r")
    file.close()
    errors = add_nurses_from_csv(path)
    for error in errors:
        print(error)
except IOError:
    print("No nurse file (%s) found" % path)

path = input("\nInput patient file name: ")
try:
    file = open(path, "r")
    file.close()
    errors = add_patients_from_csv(path)
    for error in errors:
        print(error)
except IOError:
    print("No patient file (%s) found" % path)

path = input("\nInput medical records file name: ")
try:
    file = open(path, "r")
    file.close()
    errors = add_emr_from_csv(path)
    for error in errors:
        print(error)
except IOError:
    print("No emr file (%s) found" % path)
