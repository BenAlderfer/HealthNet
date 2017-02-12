from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import *
from django.http import HttpResponse
from .models import *
from .forms import *
from datetime import datetime
from healthnet.models import *
import json


def insurance_warning(request):
    """
    this page comes up when a patient selects the option to register,
    it informs them that they should have insurance to continue
    """
    return render(request, 'users/insurance_warning.html', {})


def patient_confirmed(request):
    """
    lets user know that registration was successful
    """
    return render(request, 'users/patient_confirmed.html', {})


def staff_confirmed(request):
    """
    lets user know that registration was successful
    """
    return render(request, 'users/staff_confirmed.html', {})


def patient_register(request):
    """
    page to reqister as a patient
    """

    from emr.forms import VitalsRegForm

    user = request.user

    # If there's a user signed in, redirect them to the dashboard.
    if user.is_superuser:
        return redirect('/admin/')

    if user.id is not None:
        return redirect('/healthnet/')

    if request.method == "POST":
        # print post info for debugging
        # print (request.POST)

        form = PatientForm(data=request.POST, user=user)

        if request.POST.get('password') != request.POST.get('password_confirm'):
            form.errors['password'] = 'Password and password confirmation do ' \
                                      'not match.'

            return HttpResponse(
                json.dumps({'valid': False, 'form_errors': form.errors}),
                content_type="application/json"
            )

        if u_models.User.objects.filter(
                username=request.POST.get('email')).count() != 0:
            form.errors['email'] = 'That email address is already taken.'

            return HttpResponse(
                json.dumps({'valid': False, 'form_errors': form.errors}),
                content_type="application/json"
            )

        if form.is_valid():
            patient = form.save()

            # Generate a notification if doctor is full
            if patient.dr.at_max_patients():

                from healthnet.models import Notification

                notification = Notification(
                    receiver=patient.hospital.admins_list.all()[0],
                    message='Doctor %s has reached maximum capacity' % (
                        patient.dr.__str__()
                    ),
                    related_action='/users/manage/%i' % patient.dr.pk)
                notification.save()

            # Throw a high-capacity warning
            elif patient.dr.at_high_capacity():
                from healthnet.models import Notification

                notification = Notification(
                    receiver=patient.hospital.admins_list.all()[0],
                    message='Doctor %s is nearing maximum capacity' % (
                        patient.dr.__str__()
                    ),
                    related_action='/users/manage/%i' % patient.dr.pk)
                notification.save()

            if request.POST.get('e_contact'):
                contact = Patient.objects.get(pk=request.POST.get('e_contact'))
                patient.e_first_name = contact.first_name
                patient.e_last_name = contact.last_name
                patient.e_phone = contact.phone

            # Generate a log event
            event = ChangelogEntry(
                hospital=patient.hospital,
                time=datetime.now(),
                generatedby=patient,
                description='Patient %s Added' % patient.__str__()
            )
            event.save()

            v_form = VitalsRegForm(data=request.POST, user=user)

            if v_form.is_valid():

                # If the record is empty, don't create it.
                if not (v_form.cleaned_data['height'] or
                        v_form.cleaned_data['weight'] or
                        v_form.cleaned_data['blood_pressure_str'] != '' or
                        v_form.cleaned_data['heart_rate'] or
                        v_form.cleaned_data['cholesterol']):
                    patient.save()
                    event.save()
                    
                    return HttpResponse(
                        json.dumps({'valid': True}),
                        content_type="application/json"
                    )

                vitals = super(VitalsRegForm, v_form).save(commit=False)

                vitals.height = v_form.cleaned_data['height']
                vitals.weight = v_form.cleaned_data['weight']
                vitals.blood_pressure_str = \
                    v_form.cleaned_data['blood_pressure_str']
                vitals.cholesterol = v_form.cleaned_data['cholesterol']
                vitals.heart_rate = v_form.cleaned_data['heart_rate']

                vitals.emr = patient.emr
                vitals.created_by = patient
                vitals.date_time = datetime.now()
                vitals.is_released_to_patient = True
                vitals.save()

                # This form was valid, so save the patient and log entry
                patient.save()
                event.save()

                event = ChangelogEntry(
                    hospital=patient.hospital,
                    time=datetime.now(),
                    generatedby=patient,
                    description='Vitals Record Added for %s' \
                                % patient.__str__()
                )
                event.save()

            return HttpResponse(
                json.dumps({'valid': True}),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({'valid': False, 'form_errors': form.errors}),
                content_type="application/json"
            )

    # The doctor list has to be filtered by activity and availability
    doctor_list = [a for a in Doctor.objects.filter(is_active=True)]

    for doctor in doctor_list:
        if doctor.at_max_patients():
            doctor_list.remove(doctor)

    return render(request, 'users/patient_register.html',
                  {'hospital_list': Hospital.objects.all(),
                   'doctor_list': doctor_list,
                   'patient_list': Patient.objects.filter(is_active=True)})


def staff_register(request):
    """
    page to register as a staff member
    """

    user = request.user

    if request.method == "POST":
        # print post info for debugging
        # print (request.POST)

        role = request.POST.get('role')

        if role == "doctor":
            form = DoctorForm(data=request.POST, user=request.user)

            # make sure password matches confirmation
            if request.POST.get('password') != request.POST.get(
                    'password_confirm'):
                form.errors[
                    'password'] = 'Password and confirmation do not match'

                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

            if u_models.User.objects.filter(
                    username=request.POST.get('email')).count() != 0:
                form.errors['email'] = 'That email address is already taken'

                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

            if form.is_valid():
                doctor = form.save()
                hospital = Hospital.objects.get(pk=request.POST.get('hospital'))
                doctor.hospitals_list.add(hospital)

                # Generate a log event
                event = ChangelogEntry(
                    hospital=doctor.hospitals_list.all()[0],
                    time=datetime.now(),
                    generatedby=doctor,
                    description='Doctor %s Added' % doctor.__str__()
                )
                event.save()

                for a in HospitalAdmin.objects.filter(hospital=hospital):
                    notification = Notification(
                        receiver=a,
                        message='Doctor %s %s awaiting approval' %
                                (doctor.first_name, doctor.last_name),
                        related_action='/healthnet/doctor/%s/' % doctor.pk
                    )
                    notification.save()

                return HttpResponse(
                    json.dumps({'valid': True}),
                    content_type="application/json"
                )
            else:
                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

        elif role == "nurse":
            form = NurseForm(data=request.POST, user=request.user)

            if u_models.User.objects.filter(
                    username=request.POST.get('email')).count() != 0:
                form.errors['email'] = 'That email address is already taken'

                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

            # make sure password matches confirmation
            if request.POST.get('password') != request.POST.get(
                    'password_confirm'):
                form.errors[
                    'password'] = 'Password and confirmation do not match'

                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

            if form.is_valid():
                nurse = form.save()

                event = ChangelogEntry(
                    hospital=nurse.hospital,
                    time=datetime.now(),
                    generatedby=nurse,
                    description='Nurse %s Added' % nurse.__str__()
                )
                event.save()

                for a in \
                        HospitalAdmin.objects.filter(hospital=nurse.hospital):
                    notification = Notification(
                        receiver=a,
                        message=("Nurse, %s %s awaiting approval" %
                                 (nurse.first_name, nurse.last_name)),
                        related_action='/healthnet/nurse/%s/' % nurse.pk
                    )
                    notification.save()

                return HttpResponse(
                    json.dumps({'valid': True}),
                    content_type="application/json"
                )
            else:
                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

        elif role == "admin":
            form = AdminForm(data=request.POST, user=request.user)

            if u_models.User.objects.filter(
                    username=request.POST.get('email')).count() != 0:
                form.errors['email'] = 'That email address is already taken'

                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

            # make sure password matches confirmation
            if request.POST.get('password') != request.POST.get(
                    'password_confirm'):
                form.errors[
                    'password'] = 'Password and confirmation do not match'

                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

            if form.is_valid():
                admin = form.save()

                event = ChangelogEntry(
                    hospital=admin.hospital,
                    time=datetime.now(),
                    generatedby=admin,
                    description='Admin %s Added' % admin.__str__()
                )
                event.save()

                return HttpResponse(
                    json.dumps({'valid': True}),
                    content_type="application/json"
                )
            else:
                return HttpResponse(
                    json.dumps({'valid': False, 'form_errors': form.errors}),
                    content_type="application/json"
                )

                # generate a notification for the doctor

        else:  # no role is selected
            form = AdminForm(data=request.POST, user=request.user)
            form.errors['occupation'] = 'No occupation was selected'
            return HttpResponse(
                json.dumps({'valid': False, 'form_errors': form.errors}),
                content_type="application/json"
            )

    # If there's a user signed in, redirect them to the dashboard.
    if user.is_superuser:
        return redirect('/admin/')

    if user.id is not None:
        return redirect('/healthnet/')

    return render(request, 'users/staff_register.html',
                  {'user': user, 'hospital_list': Hospital.objects.all()})


def profile(request):
    """
    page for modifying user profile
    """

    user = request.user

    if user.id is None:
        return redirect('/healthnet/')

    if user.is_superuser:
        return redirect('/admin')

    # Get the specific instance of this user
    user = get_user_inst(user)
    notif_list = user.get_notifications()

    if is_patient(user):
        # Display patient modification form

        if request.method == "POST":

            errors = {}

            if request.POST.get('password') != '' and len(
                    request.POST.get('password')) < 8:
                errors['Password'] = "Password must contain at least 8 characters"

            if request.POST.get('password') != request.POST.get('password-confirm'):
                errors['Password Confirmation'] = "New password does not match password confirmation"

            if u_models.User.objects.filter(username=request.POST.get('email')).count():

                # This email address is taken, and not by this user.
                if request.POST.get('email') != user.username:
                    errors['Email Address'] = "That email address is already taken"

            if errors:
                return render(request, "healthnet/form_validation_error.html",
                              {'form_errors': errors})

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.username = request.POST.get('email')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.gender = request.POST.get('gender')
            user.address = request.POST.get('address')

            user.e_first_name = request.POST.get('e_first_name')
            user.e_last_name = request.POST.get('e_last_name')
            user.e_phone = request.POST.get('e_phone')


            if request.POST.get('password') is not '':
                    user.set_password(request.POST.get('password'))

            user.save()

            # Add a changelog event
            event = ChangelogEntry(
                hospital=user.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Patient %s Edited' % user.__str__()
            )
            event.save()

            if request.POST.get('password') is not '':
                return redirect('/healthnet/login')

            return redirect('/healthnet/dashboard')

        return render(request, 'users/patient_profile.html', {'user': user})

    else:
        # Display staff modification form

        if request.method == "POST":

            errors = {}

            if request.POST.get('password') != '' and len(
                    request.POST.get('password')) < 8:
                errors['Password'] = "Password must contain at least 8 characters"

            if request.POST.get('password') != request.POST.get('password-confirm'):
                errors['Password Confirmation'] = "New password does not match password confirmation"

            if u_models.User.objects.filter(
                username=request.POST.get('email')).count():

                # This email address is taken, and not by this user.
                if request.POST.get('email') != user.username:
                    errors['Email Address'] = "That email address is already taken"

            if errors:
                return render(request, "healthnet/form_validation_error.html",
                              {'form_errors': errors})

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.username = request.POST.get('email')
            user.phone = request.POST.get('phone')

            if request.POST.get('password') is not '':
                user.set_password(request.POST.get('password'))

            user.save()

            if request.POST.get('password') is not '':
                update_session_auth_hash(request, request.user)

            if is_admin(user):
                # Add a changelog event
                event = ChangelogEntry(
                    hospital=user.hospital,
                    time=datetime.now(),
                    generatedby=user,
                    description='Administrator %s Edited' % user.__str__()
                )
                event.save()

            if is_doctor(user):
                # Add a changelog event
                event = ChangelogEntry(
                    hospital=user.hospitals_list.all()[0],
                    time=datetime.now(),
                    generatedby=user,
                    description='Doctor %s Edited' % user.__str__()
                )
                event.save()

            if is_nurse(user):
                # Add a changelog event
                event = ChangelogEntry(
                    hospital=user.hospital,
                    time=datetime.now(),
                    generatedby=user,
                    description='Nurse %s Edited' % user.__str__()
                )
                event.save()

            if request.POST.get('password') is not '':
                return redirect('/healthnet/login')

            return redirect('/healthnet/dashboard')

        is_staff = not is_patient(user)

        return render(request, 'users/staff_profile.html', {'user': user,
                                                            'notif_list':
                                                                notif_list,
                                                            'is_staff':
                                                                is_staff})


def log(request, pk, page=1):
    """
    Return the event log for hospital administered by admin pk
    """

    if request.user.id is None:
        return redirect('/healthnet/')

    if int(request.user.pk) != int(pk):
        return render(request, '/healthnet/denied.html')

    if HospitalAdmin.objects.filter(pk=pk).count() != 1:
        return render(request, '/healthnet/404.html')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()
    hospital = user.hospital

    logs = ChangelogEntry.objects.filter(hospital=hospital)
    logs = [a for a in logs.order_by('-time')]

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

            for item in logs:
                valid = False

                date = item.time.date()

                if date2 <= date <= date1:
                    valid = True
                if date1 <= date <= date2:
                    valid = True

                if not valid:
                    to_remove.append(item)

            for item in to_remove:
                logs.remove(item)

    # If we're past the end of the log
    if len(logs) < (int(page) - 1) * 10:
        page = 1

    first = False
    last = False

    if int(page) == 1:
        first = True

    if int(page)*10 >= len(logs):
        last = True

    if first and last:
        log_trimmed = logs[0:len(logs)]
    elif last:
        log_trimmed = logs[(int(page)-1)*10:len(logs)]
    else:
        log_trimmed = logs[(int(page)-1)*10:int(page)*10]

    is_staff = not is_patient(user)

    return render(request, 'users/log.html', {'hospital': hospital,
                                              'log': log_trimmed,
                                              'first': first, 'pk': pk,
                                              'last': last, 'page': page,
                                              'prev': int(page) - 1,
                                              'next': int(page) + 1,
                                              'notif_list': notif_list,
                                              'is_staff': is_staff})


def manage(request, pk):
    """
    Page for a hospital admin to manage a doctor
    :param pk: The doctor's private key
    :return:
    """

    if request.user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    doctor = get_object_or_404(Doctor, pk=pk)
    patient_list = doctor.patients_list.all()
    nurse_list = doctor.nurses_list.all()

    if request.method == 'POST':

        # The "add hospital" section
        if request.POST.get("+hospital"):
            new_hosp = Hospital.objects.get(pk=request.POST["+hospital"])
            doctor.hospitals_list.add(new_hosp)
            doctor.save()

            event = ChangelogEntry(
                hospital=new_hosp,
                time=datetime.now(),
                generatedby=user,
                description='Doctor %s assigned to %s'
                            % (doctor.__str__(), new_hosp)
            )
            event.save()

        # The "remove hospital" section
        if request.POST.get("-hospital"):
            new_hosp = Hospital.objects.get(pk=request.POST["-hospital"])
            doctor.hospitals_list.remove(new_hosp)
            doctor.save()

            event = ChangelogEntry(
                hospital=new_hosp,
                time=datetime.now(),
                generatedby=user,
                description='Doctor %s removed from %s'
                            % (doctor.__str__(), new_hosp)
            )
            event.save()

            if new_hosp == user.hospital:
                return redirect("/h_admin/%s" % user.pk)

        # The "add patient" section
        if request.POST.get("+patient"):
            new_pat = Patient.objects.get(
                pk=request.POST["+patient"])
            new_pat.dr = doctor
            new_pat.save()

            event = ChangelogEntry(
                hospital=user.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Patient %s assigned to Dr. %s'
                            % (new_pat.__str__(), doctor.__str__())
            )
            event.save()

        # The "max patients" section
        if request.POST.get("maximum"):
            new_num = request.POST["maximum"]

            event = ChangelogEntry(
                hospital=user.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Dr. %s patient limit changed from %i to %i'
                            % (doctor.__str__(), doctor.max_num_patients,
                               int(new_num))
            )

            doctor.max_num_patients = int(new_num)
            doctor.save()

            event.save()

        # The "add nurse" section
        if request.POST.get("+nurse"):
            new_nurse = Nurse.objects.get(
                pk=request.POST["+nurse"])
            new_nurse.doctors_list.add(doctor)
            new_nurse.save()

            event = ChangelogEntry(
                hospital=user.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Nurse %s assigned to Dr. %s'
                            % (new_nurse.__str__(), doctor.__str__())
            )
            event.save()

        # The "remove nurse" section
        if request.POST.get("-nurse"):
            new_nurse = Nurse.objects.get(
                pk=request.POST["-nurse"])
            new_nurse.doctors_list.remove(doctor)
            new_nurse.save()

            event = ChangelogEntry(
                hospital=user.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Nurse %s removed from Dr. %s'
                            % (new_nurse.__str__(), doctor.__str__())
            )
            event.save()

        return redirect("/users/manage/%s" % pk)

    if not is_admin(user):
        return render(request, "healthnet/denied.html")

    invalid = True
    for hosp in doctor.hospitals_list.all():
        if hosp == user.hospital:
            invalid = False

    if invalid:
        return render(request, "healthnet/denied.html")

    hospital_patients = [a for a in user.hospital.patients_list.all()]
    hospital_nurses = [a for a in user.hospital.nurses_list.all()]
    hospitals = [a for a in Hospital.objects.all()]

    assigned_patients = doctor.patients_list.all()
    assigned_hospitals = doctor.hospitals_list.all()
    assigned_nurses = doctor.nurses_list.all()

    to_remove = []

    # Find unassigned patients, nurses, hospitals
    # Build list of what to remove, then remove it
    for patient in hospital_patients:
        if patient in assigned_patients:
            to_remove.append(patient)

    for patient in to_remove:
        hospital_patients.remove(patient)

    to_remove = []

    for nurse in hospital_nurses:
        if nurse in assigned_nurses:
            to_remove.append(nurse)

    for nurse in to_remove:
        hospital_nurses.remove(nurse)

    to_remove = []

    for hospital in hospitals:
        if hospital in assigned_hospitals:
            to_remove.append(hospital)

    for hospital in to_remove:
        hospitals.remove(hospital)

    is_staff = not is_patient(user)

    return render(request, "users/staff_manage.html",
                  {"hosp_assigned": assigned_hospitals,
                   "hosp_unassigned": hospitals,
                   "num_patients": doctor.get_num_patients(),
                   "pat_assigned" : assigned_patients,
                   "pat_unassigned": hospital_patients,
                   "nur_assigned": assigned_nurses,
                   "nur_unassigned": hospital_nurses,
                   "doctor": doctor,
                   "notif_list": notif_list,
                   'is_staff': is_staff
                   })


def patients(request, doctor=None, hospital=None, search=None):
    """
    Return a patients directory based on the current user
    """

    user = request.user
    if user.id is None:
        return redirect("/healthnet/")

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    if is_patient(user):
        return redirect('/permission_denied/')

    if request.method == 'POST':

        key_string = ""

        # Append the search/filter arguments
        if request.POST.get("doctor"):
            key_string += ("d_" + request.POST["doctor"])

        if request.POST.get("hospital"):
            key_string += ("h_" + request.POST["hospital"])

        if request.POST.get("contains"):
            key_string += ("c_" + request.POST["contains"])

        return redirect("/users/patients/" + key_string)

    search_string = ""

    patients_list = []
    hospital_list = []
    doctor_list = []

    if is_nurse(user):
        patients_list = user.patients_list
        hospital_list.append(user.hospital)
        doctor_list = user.doctors_list.all()
    is_dr = False
    if is_doctor(user):
        patients_list = [a for a in user.patients_list.all()]

        for pat in user.admitted_patient_list.all():
            if pat not in patients_list:
                patients_list.append(pat)

        hospital_list = [a for a in user.hospitals_list.all()]

        # Add more hospitals if the doctor is handling transfer patients
        for pat in patients_list:
            if pat.hospital not in hospital_list:
                hospital_list.append(pat.hospital)

        doctor_list.append(user)
        is_dr = True

    if is_admin(user):
        patients_list = user.hospital.patients_list.all()
        hospital_list.append(user.hospital)
        doctor_list = user.hospital.doctors_list.all()

    patients_list = [a for a in patients_list]
    doctor_list = [a for a in doctor_list]
    hospital_list = [a for a in hospital_list]

    # If we were given a doctor to sort by
    if doctor:
        dr = get_object_or_404(Doctor, pk=doctor)

        new_patients_list = []
        for patient in patients_list:
            if patient.dr == dr:
                new_patients_list.append(patient)

        patients_list = new_patients_list

        search_string += "Doctor: " + dr.first_name + " " + dr.last_name

    # If we were given a hospital to sort by
    if hospital:
        if doctor:
            search_string += " -- "

        hosp = get_object_or_404(Hospital, pk=hospital)

        new_patients_list = []
        for patient in patients_list:
            if patient.hospital == hosp:
                new_patients_list.append(patient)

        patients_list = new_patients_list

        search_string += "Hospital: " + hosp.name + '\n'

    #  If we were given a search term
    if search:

        if hospital or (doctor and not hospital):
            search_string += " -- "

        patient_list_temp = [a for a in patients_list]
        for patient in patients_list:
            if not (search.lower() in ', '.join((patient.last_name.lower(),
                    patient.first_name.lower())) or search.lower() in ' '.join(
                    (patient.first_name.lower(), patient.last_name.lower()))):
                patient_list_temp.remove(patient)

        patients_list = patient_list_temp

        search_string += "Name Contains: \"" + search + "\"\n"

    is_staff = not is_patient(user)

    return render(request, "users/patients.html",
                  {"patient_list": patients_list,
                   "doctor_list": doctor_list,
                   "hospital_list": hospital_list,
                   "search_string": search_string,
                   "is_dr": is_dr, 'notif_list' : notif_list,
                   'is_staff':is_staff})

def csv_upload(request):
    """
    Display the form for uploading a csv file containing records
    """
    from .forms import CSVImportForm
    import os

    user = request.user
    if user.id is None:
        return redirect("/healthnet")

    user = get_user_inst(user)

    if not is_admin(user):
        return redirect('/permission_denied/')

    if request.method == 'POST':

        if request.POST.get('type'):

            form = CSVImportForm(request.POST, request.FILES)
            if form.is_valid():

                file = form.cleaned_data['csvfile']

                # Write the file to somewhere permanent
                path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    '..\\media\\uploads\\tmp_csv.txt')
                with open(path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                type = request.POST['type']

                errors = []

                if type == "patients":
                    errors = user.add_patients_from_csv(path)
                elif type == "doctors":
                    errors = user.add_doctors_from_csv(path)
                elif type == "nurses":
                    errors = user.add_nurses_from_csv(path)
                elif type == "records":
                    errors = user.add_emr_from_csv(path)

                os.remove(path)

                print(errors)

                if errors:
                    return render(request, 'healthnet/upload_error.html',
                                  {'error_list': errors})
                else:
                    return render(request, 'healthnet/upload_success.html')

            else:
                return render(request, 'healthnet/form_validation_error.html',
                                  {'form_errors': form.errors})

        # Otherwise, we're downloading
        if request.POST.get('dtype'):
            dtype = request.POST['dtype']

            path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                '..\\media\\downloads\\tmp_csv.txt')

            name = ''

            if dtype == 'patients':
                user.write_patients_to_csv(path)
                name = "patients.csv"
            elif dtype == 'doctors':
                user.write_doctors_to_csv(path)
                name = "doctors.csv"
            elif dtype == 'nurses':
                user.write_nurses_to_csv(path)
                name = "nurses.csv"
            else:
                user.write_emr_to_csv(path)
                name = "emr.csv"

            dl_file = open(path, 'r')

            response = HttpResponse(dl_file.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment;filename=%s' % name

            # Delete the file for security reasons
            dl_file.close()
            os.remove(path)

            return response

    return render(request, "users/csv_up.html")
