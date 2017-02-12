from django.shortcuts import render, redirect, get_object_or_404
# from .models import *
# from healthnet.models import *
from .forms import *
import mimetypes
from django.http import HttpResponse
import os
from datetime import datetime


def vitals(request, pk):
    """
    display patient vitals
    """
    user = request.user
    can_edit = False
    if user.id is None:
        return redirect('/healthnet/')

    if user.is_superuser:
        return redirect('/admin/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    patient = get_object_or_404(Patient, pk=pk)

    if is_patient(user):
        if user.id != patient.id:
            return redirect('/permission_denied/')
    elif is_nurse(user):
        can_look = False
        patient_list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in patient_list:
            if item.id == patient.id:
                can_look = True
                can_edit = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
                can_edit = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        patient_list = user.patients_list.all()
        for item in patient_list:
            if item.id == patient.id:
                can_look = True
                can_edit = True
        if patient.admitted_dr == user:
            can_look = True
            can_edit = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_admin(user):
        if patient.hospital != user.hospital:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    emr_list = patient.emr.emritems_list.order_by('-date_time')
    emr_list_2 = []
    for item in emr_list:
        if Vitals.objects.filter(pk=item.pk).count() == 1:
            emr_list_2.append(Vitals.objects.get(pk=item.pk))

    show_all = True
    if is_patient(user):
        show_all = False
    is_staff = not is_patient(user)
    return render(request, 'emr/vitals.html',
                  {'user': user, 'page_owner': patient,
                   'vital_list': emr_list_2, 'show_all': show_all,
                   'notif_list': notif_list, 'is_staff': is_staff,
                   'can_edit': can_edit
                   })


def tests(request, pk):
    """
    display patient tests
    """
    user = request.user
    can_edit = False
    if user.id is None:
        return redirect('/healthnet/')

    if user.is_superuser:
        return redirect('/admin/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    patient = get_object_or_404(Patient, pk=pk)

    if is_patient(user):
        if user.id != patient.id:
            return redirect('/permission_denied/')
    elif is_nurse(user):
        can_look = False
        patient_list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in patient_list:
            if item.id == patient.id:
                can_look = True
                can_edit = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
                can_edit = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        patient_list = user.patients_list.all()
        for item in patient_list:
            if item.id == patient.id:
                can_look = True
                can_edit = True
        if patient.admitted_dr == user:
            can_look = True
            can_edit = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_admin(user):
        if patient.hospital != user.hospital:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    emr_list = patient.emr.emritems_list.order_by('-date_time')
    emr_list_2 = []
    for item in emr_list:
        if Test.objects.filter(pk=item.pk).count() == 1:
            emr_list_2.append(Test.objects.get(pk=item.pk))

    show_all = True
    if is_patient(user):
        show_all = False

    is_staff = not is_patient(user)

    return render(request, 'emr/tests.html', {'user': user,
                                              'page_owner': patient,
                                              'test_list': emr_list_2,
                                              'show_all': show_all,
                                              'notif_list': notif_list,
                                              'is_staff': is_staff,
                                              'can_edit': can_edit})


def prescriptions(request, pk):
    """
    display patient prescriptions
    """
    user = request.user
    can_edit = False
    if user.id is None:
        return redirect('/healthnet/')

    if user.is_superuser:
        return redirect('/admin/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    patient = get_object_or_404(Patient, pk=pk)

    if is_patient(user):
        if user.id != patient.id:
            return redirect('/permission_denied/')
    elif is_nurse(user):
        can_look = False
        emr_list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in emr_list:
            if item.id == patient.id:
                can_look = True
                can_edit = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
                can_edit = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        emr_list = user.patients_list.all()
        for item in emr_list:
            if item.id == patient.id:
                can_look = True
                can_edit = True
        if patient.admitted_dr == user:
            can_look = True
            can_edit = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_admin(user):
        if patient.hospital != user.hospital:
            return redirect('/permission_denied/')

    emr_list = patient.emr.emritems_list.order_by('-date_time')
    emr_list_2 = []
    for item in emr_list:
        if Prescription.objects.filter(pk=item.pk).count() == 1:
            emr_list_2.append(Prescription.objects.get(pk=item.pk))

    show_all = True
    if is_patient(user):
        show_all = False

    is_staff = not is_patient(user)
    return render(request, 'emr/prescriptions.html',
                  {'user': user, 'page_owner': patient,
                   'prescription_list': emr_list_2, 'show_all': show_all,
                   'notif_list': notif_list, 'is_staff': is_staff,
                   'can_edit': can_edit})


def notes(request, pk):
    """
    display patient notes
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    can_edit = False

    if user.is_superuser:
        return redirect('/admin/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    patient = get_object_or_404(Patient, pk=pk)

    if is_patient(user):
        if user.id != patient.id:
            return redirect('/permission_denied/')
    elif is_nurse(user):
        can_look = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
                can_edit = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
                can_edit = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
                can_edit = True

        if patient.admitted_dr == user:
            can_look = True
            can_edit = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_admin(user):
        if patient.hospital != user.hospital:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    emr_list = patient.emr.emritems_list.order_by('-date_time')
    list = []
    for item in emr_list:
        if Note.objects.filter(pk=item.pk).count() == 1:
            list.append(Note.objects.get(pk=item.pk))

    show_all = True
    if is_patient(user):
        show_all = False

    is_staff = not is_patient(user)
    can_edit = is_doctor(user) or is_nurse(user)

    return render(request, 'emr/notes.html', {'user': user,
                                              'page_owner': patient,
                                              'note_list': list,
                                              'show_all': show_all,
                                              'notif_list': notif_list,
                                              'is_staff': is_staff,
                                              'can_edit': can_edit})


def emr(request, pk):
    """
    display patient emr
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    if user.is_superuser:
        return redirect('/admin/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    patient = get_object_or_404(Patient, pk=pk)

    if is_patient(user):
        if user.id != patient.id:
            return redirect('/permission_denied/')
    elif is_nurse(user):
        can_look = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_admin(user):
        if patient.hospital != user.hospital:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    emr_list = patient.emr.emritems_list.order_by('-date_time')

    emr_code_list = []
    for item in emr_list:
        code = None
        emr_item = None
        if Vitals.objects.filter(pk=item.pk).count() == 1:
            code = 'v'
            emr_item = Vitals.objects.get(pk=item.pk)
        if Test.objects.filter(pk=item.pk).count() == 1:
            code = 't'
            emr_item = Test.objects.get(pk=item.pk)
        if Prescription.objects.filter(pk=item.pk).count() == 1:
            code = 'p'
            emr_item = Prescription.objects.get(pk=item.pk)
        if Note.objects.filter(pk=item.pk).count() == 1:
            code = 'n'
            emr_item = Note.objects.get(pk=item.pk)
        if Admission.objects.filter(pk=item.pk).count() == 1:
            code = 'a'
            emr_item = Admission.objects.get(pk=item.pk)
        if Discharge.objects.filter(pk=item.pk).count() == 1:
            code = 'd'
            emr_item = Discharge.objects.get(pk=item.pk)
        if Transfer.objects.filter(pk=item.pk).count() == 1:
            code = 'tr'
            emr_item = Transfer.objects.get(pk=item.pk)
        emr_code_list.append({'code': code, 'item': emr_item})

    show_all = (not is_patient(user))

    from healthnet.models import ChangelogEntry

    # This is sensitive - log it
    entry = ChangelogEntry(hospital=patient.hospital,
                           time=datetime.now(),
                           generatedby=user,
                           description="Medical records of %s viewed." %
                                       patient.__str__()
                           )

    entry.save()

    is_staff = not is_patient(user)
    can_edit = is_doctor(user) or is_nurse(user)

    if request.method == 'POST':
        # Filter if we got a date set
        try:
            date1 = datetime.strptime(request.POST.get('startdate'), '%m-%d-%Y')
        except:
            try:
                date1 = datetime.strptime(request.POST.get('startdate'),
                                          '%m-%d-%y')
            except:
                try:
                    date1 = datetime.strptime(request.POST.get('startdate'),
                                              '%Y-%m-%d')
                except:
                    date1 = None

        try:
            date2 = datetime.strptime(request.POST.get('enddate'), '%m-%d-%Y')
        except:
            try:
                date2 = datetime.strptime(request.POST.get('enddate'),
                                          '%m-%d-%y')
            except:
                try:
                    date2 = datetime.strptime(request.POST.get('enddate'),
                                              '%Y-%m-%d')
                except:
                    date2 = None

        if date1 and date2:

            date1 = date1.date()
            date2 = date2.date()

            to_remove = []

            for item in emr_code_list:
                emritem = item['item']
                valid = False

                date = emritem.date_time.date()

                if date2 <= date <= date1:
                    valid = True
                if date1 <= date <= date2:
                    valid = True

                if not valid:
                    to_remove.append(item)

            for item in to_remove:
                emr_code_list.remove(item)

    return render(request, 'emr/emr.html', {'user': user, 'page_owner': patient,
                                            'emr_list': emr_code_list,
                                            'show_all': show_all,
                                            'notif_list': notif_list,
                                            'is_staff': is_staff,
                                            'can_edit': can_edit})


def new_vital(request, pk):
    """
    add a new patient vital
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = VitalsEntryForm(data=request.POST, user=user, patientpk = pk)
        if form.is_valid():
            vital = form.save()
            if request.POST["blood_pressure_sp"] == "" or \
                    request.POST["blood_pressure_dp"] == "":
                vital.blood_pressure_str = None
            else:
                vital.blood_pressure_str = '/'.join(
                    [request.POST["blood_pressure_sp"],
                     request.POST["blood_pressure_dp"]])
            vital.save()
            patient = vital.emr.patient
            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Vital added to EMR for %s' % patient.__str__()
            )
            event.save()
            if not vital.is_released_to_patient:
                notification = Notification(
                    receiver=patient.dr,
                    message='Vital awaiting approval for patient: %s' % (
                        patient.__str__()
                    ),
                    related_action='/emr/edit_vital/%i' % vital.pk
                )
                notification.save()
            return redirect('/emr/vitals/%i' % patient.pk)
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})
    if is_nurse(user):
        can_look = False
        is_dr = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        is_dr = True
        list = user.patients_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True

        if can_look is False:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    is_staff = not is_patient(user)

    return render(request, 'emr/new_vital.html', {'user': user,
                                                  'patient': patient,
                                                  'is_dr': is_dr,
                                                  'notif_list': notif_list,
                                                  'is_staff':is_staff})


def edit_vital(request, pk):
    """
    edit a previous instance of a patients vitals
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    vital = get_object_or_404(Vitals, pk=pk)
    patient = vital.emr.patient

    if request.method == 'POST':
        form = VitalsEntryForm(data=request.POST, user=user,
                               patientpk=patient.pk)
        if form.is_valid():
            if request.POST["blood_pressure_sp"] == "" or \
                            request.POST["blood_pressure_dp"] == "":
                vital.blood_pressure_str = None
            else:
                vital.blood_pressure_str = '/'.join(
                    [request.POST["blood_pressure_sp"],
                     request.POST["blood_pressure_dp"]])

            was_released = vital.is_released_to_patient

            vital.height = form.cleaned_data["height"]
            vital.weight = form.cleaned_data["weight"]
            vital.cholesterol = form.cleaned_data["cholesterol"]
            vital.heart_rate = form.cleaned_data["heart_rate"]
            vital.is_released_to_patient = \
                form.cleaned_data["is_released_to_patient"]
            vital.save()
            patient = vital.emr.patient
            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Vital edited for %s' % patient.__str__()
            )

            event.save()
            if not vital.is_released_to_patient and was_released:
                notification = Notification(
                    receiver=patient.dr,
                    message='Vital awaiting approval for patient: %s' % (
                        patient.__str__()
                    ),
                    related_action='/emr/edit_vital/%i' % vital.pk
                )
                notification.save()

            # It's released, so remove any related notifications
            elif vital.is_released_to_patient:
                notifications = Notification.objects.all()
                to_remove = []
                for notification in notifications:
                    if (request.path in notification.related_action or
                            notification.related_action in request.path) and \
                                notification.related_action != '/':
                        to_remove.append(notification)

                    for notif in to_remove:
                        notif.delete()

            return redirect('/emr/vitals/%i' % patient.pk)
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})

    if is_nurse(user):
        can_look = False
        list = user.patients_list
        is_dr = False
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        is_dr = True
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    sp = None
    dp = None
    if vital.blood_pressure_str:
        sp = vital.blood_pressure_str.split('/')[0]
        dp = vital.blood_pressure_str.split('/')[1]

    is_staff = not is_patient(user)
    return render(request, 'emr/edit_vital.html',
                  {'user': user,
                   'vital': vital,
                   'sp': sp,
                   'dp': dp,
                   'is_dr': is_dr,
                   'notif_list': notif_list,
                   'is_staff': is_staff
                   })


def new_test(request, pk):
    """
    add a new patient test
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    patient = get_object_or_404(Patient, pk=pk)
    user_is_doctor = False

    if request.method == 'POST':
        form = TestEntryForm(data=request.POST, files=request.FILES, user=user,
                             patientpk=pk)

        # Check if the uploaded file is a valid type
        if request.FILES.get('image'):
            name = request.FILES.get('image').name
            formats = ['.png', '.bmp', '.jpg', '.jpeg', '.gif']
            valid = False

            for frmt in formats:
                if frmt in name:
                    valid = True

            if not valid:
                form.errors['image'] = 'Please select an image file of type' +\
                                       ' .png, .bmp, .jpg/jpeg, or .gif.'

        if form.is_valid():
            test = form.save()
            patient = test.emr.patient

            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Test added to EMR for %s' % patient.__str__()
            )
            event.save()
            if not test.is_released_to_patient:
                notification = Notification(
                    receiver=patient.dr,
                    message='Test awaiting approval for patient: %s' % (
                        patient.__str__()
                    ),
                    related_action='/emr/edit_test/%i' % test.pk
                )
                notification.save()
            return redirect('/emr/tests/%i' % patient.pk)
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})
    if is_nurse(user):
        can_look = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        user_is_doctor = True
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    is_staff = not is_patient(user)

    return render(request, 'emr/new_test.html', {'user': user,
                                                 'patient': patient,
                                                 'is_dr': user_is_doctor,
                                                 'notif_list': notif_list,
                                                 'is_staff': is_staff})


def edit_test(request, pk):
    """
    make changes to an existing test in a patient's emr
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    test = get_object_or_404(Test, pk=pk)
    patient = test.emr.patient
    user_is_doctor = False

    if request.method == 'POST':
        form = TestEntryForm(data=request.POST, files=request.FILES, user=user,
                             patientpk = patient.pk)
        if form.is_valid():

            was_released = test.is_released_to_patient

            test.description = form.cleaned_data["description"]
            test.result = form.cleaned_data["result"]
            test.comments = form.cleaned_data["comments"]

            if request.FILES.get("image"):
                test.image = form.cleaned_data["image"]

            test.is_released_to_patient =\
                form.cleaned_data["is_released_to_patient"]
            
            test.save()
            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Test edited for %s' % patient.__str__()
            )
            event.save()

            if not test.is_released_to_patient and was_released:
                notification = Notification(
                    receiver=patient.dr,
                    message='Test awaiting approval for patient: %s' % (
                        patient.__str__()
                    ),
                    related_action='/emr/edit_test/%i' % test.pk
                )
                notification.save()

            # It's released, so remove any related notifications
            elif test.is_released_to_patient:
                notifications = Notification.objects.all()
                to_remove = []
                for notification in notifications:
                    if (request.path in notification.related_action or
                        notification.related_action in request.path) and \
                            notification.related_action != '/':
                        to_remove.append(notification)

                for notification in to_remove:
                    notification.delete()

            return redirect('/emr/tests/%i' % patient.pk)
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})
    if is_nurse(user):
        can_look = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        user_is_doctor = True
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    is_staff = not is_patient(user)

    return render(request, 'emr/edit_test.html', {'user': user,
                                                  'patient': patient,
                                                  'is_dr': user_is_doctor,
                                                  'test': test,
                                                  'notif_list': notif_list,
                                                  'is_staff': is_staff})


def new_note(request, pk):
    """
    add a new patient test
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    patient = get_object_or_404(Patient, pk=pk)
    user_is_doctor = False

    if request.method == 'POST':
        form = NotesEntryForm(data=request.POST, user=user, patientpk = pk)
        if form.is_valid():
            note = form.save()
            patient = note.emr.patient
            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Note added to EMR for %s' % patient.__str__()
            )
            event.save()
            if not note.is_released_to_patient:
                notification = Notification(
                    receiver=patient.dr,
                    message='Note awaiting approval for patient: %s' % (
                        patient.__str__()
                    ),
                    related_action='/emr/edit_note/%i' % note.pk
                )
                notification.save()
            return redirect('/emr/notes/%i' % patient.pk)
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})
    if is_nurse(user):
        can_look = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        user_is_doctor = True
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    is_staff = not is_patient(user)

    return render(request, 'emr/new_note.html', {'user': user,
                                                 'patient': patient,
                                                 'is_dr': user_is_doctor,
                                                 'notif_list': notif_list,
                                                 'is_staff': is_staff})


def edit_note(request, pk):
    """
    update a note on a patient's emr
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    note = get_object_or_404(Note, pk=pk)
    patient = note.emr.patient
    user_is_doctor = False

    if request.method == 'POST':
        form = NotesEntryForm(data=request.POST, user=user, patientpk = patient.pk)

        was_released = note.is_released_to_patient

        if form.is_valid():
            note.message = form.cleaned_data["message"]
            note.is_released_to_patient =\
                form.cleaned_data["is_released_to_patient"]
            note.save()
            patient = note.emr.patient
            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Note edited for %s' % patient.__str__()
            )
            event.save()

            if not note.is_released_to_patient and was_released:
                notification = Notification(
                    receiver=patient.dr,
                    message='Note awaiting approval for patient: %s' % (
                        patient.__str__()
                    ),
                    related_action='/emr/edit_note/%i' % note.pk
                )
                notification.save()

            elif note.is_released_to_patient:
                notifications = Notification.objects.all()
                to_remove = []
                for notification in notifications:
                    if (request.path in notification.related_action or
                            notification.related_action in request.path) and \
                            notification.related_action != '/':
                        to_remove.append(notification)

                    for notif in to_remove:
                        notif.delete()

            return redirect('/emr/notes/%i' % patient.pk)
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})
    if is_nurse(user):
        can_look = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        user_is_doctor = True
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    is_staff = not is_patient(user)

    return render(request, 'emr/edit_note.html', {'user': user,
                                                  'patient': patient,
                                                  'is_dr': user_is_doctor,
                                                  'notif_list': notif_list,
                                                  'note': note,
                                                  'is_staff': is_staff})


def new_prescription(request, pk):
    """
    add a new patient test
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    patient = get_object_or_404(Patient, pk=pk)
    user_is_doctor=False

    if request.method == 'POST':
        form = PrescriptionEntryForm(data=request.POST, user=user, patientpk = pk)
        if form.is_valid():
            prescription = form.save()
            patient = prescription.emr.patient
            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Prescription added to EMR for %s' %
                            patient.__str__()
            )
            event.save()

            if prescription.name.lower() == "^relish":
                return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

            return redirect('/emr/prescriptions/%i' % patient.pk)
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})
    if is_nurse(user):
        can_look = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        user_is_doctor = True
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    is_staff = not is_patient(user)
    return render(request, 'emr/new_prescription.html', {'user': user,
                                                         'patient': patient,
                                                         'is_dr':
                                                             user_is_doctor,
                                                         'notif_list':
                                                             notif_list,
                                                         'is_staff': is_staff
                                                         })


def edit_prescription(request, pk):
    """
    edit prescription information
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    prescription = get_object_or_404(Prescription, pk=pk)
    patient = prescription.emr.patient
    user_is_doctor = False

    if request.method == 'POST':
        form = PrescriptionEntryForm(data=request.POST, user=user,
                                     patientpk=patient.pk)

        if form.is_valid():
            prescription.dosage = form.cleaned_data["dosage"]
            prescription.quantity = form.cleaned_data["quantity"]
            prescription.units = form.cleaned_data["units"]
            prescription.name = form.cleaned_data["name"]
            prescription.save()
            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Prescription added to EMR for %s' %
                            patient.__str__()
            )
            event.save()

            if prescription.name.lower() == "^relish":
                return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

            return redirect('/emr/prescriptions/%i' % patient.pk)
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})
    if is_nurse(user):
        can_look = False
        list = user.patients_list
        doctors_list = user.doctors_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        for doc in doctors_list:
            if patient.admitted_dr == doc:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        user_is_doctor = True
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    else:
        return redirect('/permission_denied/')

    is_staff = not is_patient(user)

    return render(request, 'emr/edit_prescription.html', {'user': user,
                                                          'patient': patient,
                                                          'is_dr':
                                                              user_is_doctor,
                                                          'notif_list':
                                                              notif_list,
                                                          'prescription':
                                                              prescription,
                                                          'is_staff': is_staff})


def delete_item(request, pk):
    """
    delete any emr item from its edit menu
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    emr_item = get_object_or_404(EMRItem, pk=pk)
    patient = emr_item.emr.patient
    if is_doctor(user):
        can_look = False
        list = user.patients_list.all()
        for item in list:
            if item.id == patient.id:
                can_look = True
        if patient.admitted_dr == user:
            can_look = True
        if can_look:
            event = ChangelogEntry(
                hospital=emr_item.emr.patient.hospital,
                time=datetime.now(),
                generatedby=user,
                description='EMR Item Removed from %s' % patient
            )

            # Delete any related notifications
            notifications = Notification.objects.all()
            to_remove = []

            for notification in notifications:
                if (str(pk) in notification.related_action and
                        notification.related_action != '/'):
                    to_remove.append(notification)

            for notification in to_remove:
                notification.delete()

            event.save()
            emr_item.delete()

            return redirect('/emr/%i' % patient.pk)
    return redirect('/permission_denied')


def add_admission(request, pk):
    """
    add a new patient admission page
    :param request: when one of the buttons is clicked
    :param pk: the pk of the patient
    :return: a confirmation page or an 'already admitted' page
    """

    patient = Patient.objects.get(pk=pk)
    # patient is already admitted somewhere
    if patient.admitted is not None:
        return render(request, 'emr/already_admitted.html')

    # user not logged in
    if request.user.id is None:
        return redirect('/healthnet/')

    user = request.user
    user = get_user_inst(user)

    # user that does not exist, patients, and hospital admins cannot
    # admit patients
    if user is None or is_patient(user) or is_admin(user):
        return redirect('/permission_denied/')

    if request.method == 'POST':
        form = AdmissionForm(data=request.POST, user=user)
        if form.is_valid():
            admission = form.save()
            # get the patient
            patient = Patient.objects.get(pk=pk)
            # change patient's admitted hospital and doctor
            patient.admitted = admission.hospital
            patient.admitted_dr = admission.doctor
            patient.save()
            # get patient emr and save it to the admission
            emr = EMR.objects.get(patient=patient)
            admission.emr = emr
            admission.is_released_to_patient = True
            # get the admission reason
            admission.reason = request.POST.get('reason')
            admission.created_by = user
            # save the new admission
            admission.save()

            event = ChangelogEntry(
                hospital=admission.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Admission for %s Added' % admission.emr
            )

            if admission.reason == 'OTH':
                message = 'Patient: %s admitted to %s' % (patient,
                                                          admission.hospital)
            else:
                message = 'Patient: %s admitted to %s for %s' % (patient,
                                                            admission.hospital,
                                                            admission.reason)
            notification = Notification(
                receiver=patient.admitted_dr,
                message=message,
                related_action='/patient/%i' % patient.pk
            )
            notification.save()

            event.save()

            return render(request, 'emr/admission_confirmation.html',
                          {'patient': patient})

    # Filter fillable fields
    if is_doctor(user):
        # doctors can admit to any of their hospitals and to themselves
        return render(request, 'emr/add_admission.html',
                      {'hospital_list': user.hospitals_list.all(),
                       'is_doctor': user,
                       'reason_list': Admission.REASON_CHOICES,
                       'patient': patient
                       })

    if is_nurse(user):
        # nurses can admit to their hospital and any of their doctors
        return render(request, 'emr/add_admission.html',
                      {
                          'hospital_list': [user.hospital],
                          'is_doctor': None,
                          'reason_list': Admission.REASON_CHOICES,
                          'patient': patient
                      })

    return redirect("/permission_denied/")


def add_discharge(request, pk):
    """
    discharges a patient if they are currently admitted
    :param request:
    :param pk:
    :return:
    """
    patient = Patient.objects.get(pk=pk)


    user = request.user
    user = get_user_inst(user)

    # only current admitted doctor can discharge
    if user != patient.admitted_dr:
        return redirect('/permission_denied/')

    # the patient is not admitted anywhere so cannot be discharged
    if patient.admitted is None:
        return render(request, 'emr/not_admitted.html')

    if request.user.id is None:
        return redirect('/healthnet/')



    if request.method == 'POST':
            discharge = Discharge()
            # get patient and emr
            patient = Patient.objects.get(pk=pk)
            emr = EMR.objects.get(patient=patient)
            discharge.emr = emr
            discharge.created_by = user
            discharge.initialize()
            discharge.is_released_to_patient = True

            if is_doctor(user):

                patient.admitted = None
                patient.admitted_dr = None
                patient.save()
                discharge.save()

                event = ChangelogEntry(
                    hospital=discharge.hospital,
                    time=datetime.now(),
                    generatedby=user,
                    description='Discharge for %s Added' % discharge.emr
                )

                event.save()

                return render(request, 'emr/discharge_confirmation.html',
                              {'patient': patient})

    else:
        return render(request, 'emr/add_discharge.html',
                      {
                          'patient': patient
                      })


def add_transfer(request, pk):
    """
    A transfer page for hospital administrators and sending doctors
    :param request:
    :param pk:
    :return:
    """
    # get patient
    patient = Patient.objects.get(pk=pk)

    # only admitted patients can be transferred
    if patient.admitted is None:
        return render(request, 'emr/not_admitted.html')

    # user needs be, well, a user
    if request.user.id is None:
        return redirect('/healthnet/')

    # get the current user
    user = request.user
    user = get_user_inst(user)

    # if a transfer is most recent change in status, do not allow to transfer
    # again
    if patient.emr.latest_changeinstatus_is_transfer():
        return redirect('/permission_denied/')

    if user != patient.admitted_dr and not is_admin(user):
        return redirect('/permission_denied/')

    if request.method == 'POST':
        form = TransferForm(data=request.POST, user=user)
        if form.is_valid():
            # fill in all necessary info
            transfer = form.save()
            patient = Patient.objects.get(pk=pk)
            emr = EMR.objects.get(patient=patient)
            transfer.emr = emr
            transfer.doctor = emr.latest_admission().doctor
            transfer.hospital = emr.latest_admission().hospital
            transfer.is_released_to_patient = True
            transfer.save()

            # if created by a doctor, create a notification for the receiving
            # doctor
            if is_doctor(user):
                notification = Notification(
                    receiver=transfer.receiving_doctor,
                    message='Patient awaiting transfer to you',
                    related_action='/emr/confirm_transfer/%s/' % patient.pk
                )
                notification.save()

                event = ChangelogEntry(
                    hospital=transfer.hospital,
                    time=datetime.now(),
                    generatedby=user,
                    description='Transfer for %s Added' % transfer.emr
                )

                event.save()

                return render(request, 'emr/transfer_request_sent.html')

            # if created by admin, create an admission object as well
            elif is_admin(user):
                admission = Admission.objects.create(
                    emr=emr,
                    doctor=transfer.receiving_doctor,
                    hospital=transfer.receiving_hospital,
                    reason=emr.latest_admission().reason,
                    created_by=user
                )
                admission.save()

                patient.admitted_dr = admission.doctor
                patient.admitted = admission.hospital
                patient.save()

                event_t = ChangelogEntry(
                    hospital=transfer.hospital,
                    time=datetime.now(),
                    generatedby=user,
                    description='Transfer for %s Added' % transfer.emr
                )

                event_t.save()

                event_a = ChangelogEntry(
                    hospital=admission.hospital,
                    time=datetime.now(),
                    generatedby=user,
                    description='Admission for %s Added' % admission.emr
                )

                event_a.save()

                return render(request, 'emr/transfer_confirmation.html')

    else:
        return render(request, 'emr/add_transfer.html',
                      {
                          'hospital_list': Hospital.objects.all(),
                          'doctor_list': Doctor.objects.all(),
                          'reason_list': Transfer.REASON_CHOICES,
                          'patient': patient
                      })


def confirm_transfer(request, pk):
    """
    A simple confirmation form for receiving doctors
    :param request:
    :param pk:
    :return:
    """
    # get patient
    patient = Patient.objects.get(pk=pk)
    emr = EMR.objects.get(patient=patient)
    last_transfer = emr.latest_transfer()

    # make sure user is a user
    if request.user.id is None:
        return redirect('/healthnet/')

    # get user
    user = request.user
    user = get_user_inst(user)

    # make sure user is supposed to be the receiving doctor
    if user != last_transfer.receiving_doctor:
        return redirect('/permission_denied/')

    if request.method == 'POST':
        if request.POST['accept_decline'] == 'accept':
            # transfer accepted, create admission object
            admission = Admission.objects.create(
                emr=emr,
                doctor=emr.latest_transfer().receiving_doctor,
                hospital=emr.latest_transfer().receiving_hospital,
                reason=emr.latest_admission().reason
            )
            admission.save()

            # change patient admitted doctor and hospital
            patient.admitted = admission.hospital
            patient.admitted_dr = admission.doctor
            patient.save()

            # make a changelog entry for the new admission
            event = ChangelogEntry(
                hospital=admission.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Admission for %s Added' % admission.emr
            )

            event.save()

            # delete notification
            related_action = '/emr/confirm_transfer/%s/' % patient.pk
            Notification.objects.all().filter(related_action=related_action).\
                delete()

            return render(request, 'emr/admission_confirmation.html',
                          {'patient': patient})

        if request.POST['accept_decline'] == 'decline':
            # delete the last transfer
            emr.latest_transfer().delete()

            # delete notification
            related_action = '/emr/confirm_transfer/%s/' % patient.pk
            Notification.objects.all().filter(related_action=related_action). \
                delete()

            return redirect('/healthnet/')

    return render(request, 'emr/confirm_transfer.html', {'patient': patient})


def test_image(request, pk):
    """
    Authenticate & return image for corresponding test
    :param pk: The database key of the test
    :param request:
    """

    user = request.user
    test = get_object_or_404(Test, pk=pk)

    # Kick out non-users
    if user.id is None:
        return redirect("/healthnet")

    user = get_user_inst(user)

    denied = True

    if is_patient(user):
        if test.emr.patient == user:
            if test.is_released_to_patient:
                denied = False

    if is_nurse(user):
        if test.emr.patient in user.patients_list():
            denied = False

    if is_doctor(user):
        if test.emr.patient in user.patients_list.all():
            denied = False

    if is_admin(user):
        if test.emr.patient.hospital == user.hospital:
            denied = False

    if denied:
        return redirect("/permission_denied")

    # Passed all authentication
    image = test.image

    content_type = mimetypes.guess_type(image.name)[0]
    # Use mimetypes to get file type

    dl_file = open(image.name, 'rb')

    response = HttpResponse(dl_file.read(), content_type=content_type)
    response['Content-Disposition'] = 'inline;filename=%s' % image.name
    response['Content-Length'] = os.path.getsize(image.name)

    dl_file.close()

    return response
