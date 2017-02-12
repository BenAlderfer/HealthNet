from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import *
from django.contrib.auth import models as u_models
from django.http import HttpResponse
from itertools import chain
import json
from .models import *
from users.models import *
from .forms import *
from datetime import datetime
from django.utils import timezone
from .models import *
from emr.models import *
import operator

from datetime import timedelta
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView


def index(request):
    """
    home screen for healthnet, if a user is already logged in, redirect them
    to their dashboard
    """

    user = request.user

    # If there's a user signed in, redirect them to the dashboard.
    if user.id is not None:
        if user.is_superuser:
            return redirect('/admin')
        else:
            return redirect('/healthnet/dashboard')

    return render(request, 'healthnet/index.html', {})


def form_validation_error(request):
    """
    lets a user know that they made an error filling out a form, and
    gives them the option to return to the previous form
    """

    return render(request, 'healthnet/form_validation_error.html', {})


def logout_view(request):
    """
    returns user to healthnet homepage on logout
    """

    logout(request)
    return redirect('/healthnet/')


def login_view(request):
    """
    login page for all users
    """
    user = request.user
    if user.id is not None:
        return redirect('/healthnet/')

    if request.method == "POST":

        # Catch errors with accidental form resubmission
        if user.id is not None:
            return redirect('/healthnet/')

        email = request.POST.get('email')
        password = request.POST.get('password')

        # u = u_models.User.objects.get(username= 'jabba@huttmail.com')
        # u = get_user_inst(u)
        # print(u.password)

        user = authenticate(username=email, password=password)

        if user is None:

            # Prepare error message
            error = []

            user_exists = u_models.User.objects.filter(username=email)

            if user_exists:
                error = ["Password is incorrect."]
            else:
                error = ["Username not found."]

            return render(request, 'healthnet/login.html',
                          {'form_errors': error, 'email': email})

        elif user.is_active:
            login(request, user)
            request.META['CSRF_COOKIE_USED'] = False

            return redirect(u'/healthnet/dashboard')
        elif not user.is_active:
            error = ["Your account is pending administrator approval. Please " +
                     "check back later."]
            return render(request, 'healthnet/login.html',
                          {'form_errors': error, 'email': email})

    return render(request, 'healthnet/login.html')


def dashboard(request):
    """
    get user dashboard
    """
    if request.user.id is None:
        return redirect('/healthnet/')

    user = request.user

    if is_doctor(user):
        # Present the doctor dashboard
        user = get_user_inst(user)

        return redirect('/doctor/%i' % user.pk)

    if is_nurse(user):
        # Present the nurse dashboard
        user = get_user_inst(user)

        return redirect('/nurse/%i' % user.pk)

    if is_patient(user):
        # Present the patient dashboard
        user = get_user_inst(request.user)
        return redirect('/patient/%i' % user.pk)

    if is_admin(user):
        # Present the admin dashboard
        user = get_user_inst(request.user)
        return redirect('/h_admin/%i' % user.pk)

    if user.is_superuser:
        return redirect('/admin/')

    return redirect('/healthnet/')


def doctor_dashboard(request, pk):
    """
    get dashboard for a doctor
    """
    if request.user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(request.user)
    activate = False
    doctor = get_object_or_404(Doctor, pk=pk)
    patient_list = doctor.patients_list.all()
    nurse_list = doctor.nurses_list.all()
    notif_list = user.get_notifications()

    if request.method == 'POST':
        doctor.is_active = True
        doctor.save()

        # Note: We can assume the user is an admin because only admins see the
        # staff activation button.
        event = ChangelogEntry(
            hospital=user.hospital,
            time=datetime.now(),
            generatedby=user,
            description='Doctor %s Activated' % doctor.__str__()
        )
        event.save()

        notifications = Notification.objects.all()
        to_remove = []
        for notification in notifications:
            if (request.path in notification.related_action or
                    notification.related_action in request.path) and \
                            notification.related_action != '/':
                to_remove.append(notification)

            for notification in to_remove:
                if notification.id:
                    notification.delete()

        return redirect('/doctor/%s' % pk)

    isadmin = False
    activate = False

    if is_patient(user):
        return redirect('/permission_denied/')
    elif is_nurse(user):
        can_look = False
        for item in nurse_list:
            if item.id == user.id:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        if doctor.id != user.id:
            return redirect('/permission_denied/')
    elif is_admin(user):
        invalid = True
        activate = False
        for hosp in doctor.hospitals_list.all():
            if hosp == user.hospital:
                invalid = False

        if invalid:
            return redirect('/permission_denied/')

        isadmin = True
        if not doctor.is_active:
            # Show the activate button
            activate = True

    appts = doctor.appointments_list.order_by('date_time')

    # Ignore events that already happened
    # First convert appts to a list.
    appts = [a for a in appts]

    for appt in appts:
        if appt.date_time < timezone.now():
            appts.remove(appt)

    # And snip the first three
    appts = appts[0:3]
    patient_list = patient_list[0:3]

    hosps = doctor.hospitals_list.order_by('name')
    is_staff = not is_patient(user)

    return render(request, 'healthnet/doctor_dashboard.html',
                  {'user': user, "page_owner": doctor,
                   "patient_list": patient_list, "nurse_list": nurse_list,
                   'isadmin': isadmin, 'activate': activate, 'appt_list': appts,
                   'hospitals_list': hosps.all(), 'notif_list': notif_list,
                   'is_staff': is_staff})


def patient_dashboard(request, pk):
    if request.user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    patient = get_object_or_404(Patient, pk=pk)

    can_admit = False
    can_transfer = False
    can_discharge = False

    if is_patient(user):
        if user.id != patient.id:
            return redirect('/permission_denied/')
    elif is_nurse(user):
        can_admit = True
        can_look = False
        list = user.patients_list
        for item in list:
            if item.id == patient.id:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_doctor(user):

        can_admit = True
        can_transfer = True
        can_discharge = True

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

        can_transfer = True

        if patient.hospital != user.hospital:
            return redirect('/permission_denied/')

    emr_list = patient.emr.emritems_list.order_by('-date_time')
    vital_list = []
    test_list = []
    prescription_list = []
    note_list = []

    # Get the EMRs
    for item in emr_list:
        if item.is_released_to_patient or (not is_patient(user)):
            if Vitals.objects.filter(pk=item.pk).count() == 1:
                vital_list.append(Vitals.objects.get(pk=item.pk))
            if Test.objects.filter(pk=item.pk).count() == 1:
                test_list.append(Test.objects.get(pk=item.pk))
            if Prescription.objects.filter(pk=item.pk).count() == 1:
                prescription_list.append(Prescription.objects.get(pk=item.pk))
            if Note.objects.filter(pk=item.pk).count() == 1:
                note_list.append(Note.objects.get(pk=item.pk))

    # Take only the top 3 for concise-ness on the dashboard.
    vital_list = vital_list[0:3]
    test_list = test_list[0:3]
    prescription_list = prescription_list[0:3]
    note_list = note_list[0:3]

    appts = patient.appointments_list.order_by('date_time')

    # Ignore events that already happened
    # First convert appts to a list.
    appts = [a for a in appts]

    for appt in appts:
        if appt.date_time < timezone.now():
            appts.remove(appt)

    # And snip the first three
    appts = appts[0:3]
    no_edit = is_patient(user) or is_admin(user)
    is_staff = not is_patient(user)

    return render(request, 'healthnet/patient_dashboard.html',
                  {'user': user, 'page_owner': patient,
                   'vital_list': vital_list,
                   'test_list': test_list,
                   'prescription_list': prescription_list,
                   'note_list': note_list, 'appt_list': appts,
                   'notif_list': notif_list, 'is_patient': no_edit,
                   'can_admit': can_admit, 'can_transfer': can_transfer,
                   'can_discharge': can_discharge, 'is_staff': is_staff})


def nurse_dashboard(request, pk):
    """
    Get a nurse dashboard.
    This can be done by the nurse themself, or any doctor
    or hospital admin associated with that nurse
    """
    if request.user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    nurse = get_object_or_404(Nurse, pk=pk)
    doctor_list = nurse.doctors_list.all()

    if request.method == 'POST':
        nurse.is_active = True
        nurse.save()

        event = ChangelogEntry(
            hospital=user.hospital,
            time=datetime.now(),
            generatedby=user,
            description='Nurse %s Activated' % nurse.__str__()
        )
        event.save()

        # Remove any notifications related to releasing this staff member
        notifications = Notification.objects.all()
        to_remove = []
        for notification in notifications:
            if (request.path in notification.related_action or
                    notification.related_action in request.path) and \
                            notification.related_action != '/':
                to_remove.append(notification)

            for notification in to_remove:
                if notification.id:
                    notification.delete()

        return redirect('/nurse/%s' % pk)

    isadmin = False

    if is_patient(user):
        return redirect('/permission_denied/')
    elif is_nurse(user):
        if nurse.id != user.id:
            return redirect('/permission_denied/')
    elif is_doctor(user):
        can_look = False
        for item in doctor_list:
            if item.id == user.id:
                can_look = True
        if can_look is False:
            return redirect('/permission_denied/')
    elif is_admin(user):
        if nurse.hospital != user.hospital:
            return redirect('/permission_denied/')
        if not nurse.is_active:
            isadmin = True

    appts = []
    for doc in nurse.doctors_list.all():
        appts += list(Appointment.objects.filter(doctor=doc))
    appts = \
        sorted(appts, key=lambda appointment: appointment.date_time)
    for appt in appts:
        if appt.date_time < timezone.now():
            appts.remove(appt)
        else:
            break

    appts = appts[0:3]
    is_staff = not is_patient(user)

    return render(request, 'healthnet/nurse_dashboard.html',
                  {'user': user, 'page_owner': nurse, 'doctor_list':
                      doctor_list, 'isadmin': isadmin, 'appt_list': appts,
                      'notif_list': notif_list, 'is_staff': is_staff})


def admin_dashboard(request, pk):
    """
    get a hospital administrator dashboard
    """
    # Present the admin dashboard
    if request.user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()

    # Get relevant lists
    h = user.hospital

    dlist = h.doctors_list.all()
    nlist = h.nurses_list.all()
    appts = h.appointments_list.all()

    a_doctors = h.doctors_list.filter(is_active=False).all()
    a_nurses = h.nurses_list.filter(is_active=False).all()

    user = get_user_inst(request.user)
    admin = get_object_or_404(HospitalAdmin, pk=pk)

    if user.id != admin.id:
        return redirect('/permission_denied')

    appts = list(appts)

    for appt in appts:
        if appt.date_time < timezone.now():
            appts.remove(appt)

    # And snip the first three
    appts = appts[0:3]

    hospital = admin.hospital
    logs = ChangelogEntry.objects.filter(hospital=hospital)
    logs = logs.order_by('-time')

    if logs.count() < 3:
        logs = logs[0:logs.count()]
    else:
        logs = logs[0:3]

    is_staff = not is_patient(user)

    return render(request, 'healthnet/admin_dashboard.html',
                  {'user': user, 'page_owner': admin,
                   'doctor_list': dlist, 'nurse_list': nlist,
                   'a_nurses': a_nurses, 'a_doctors': a_doctors,
                   'appt_list': appts,
                   'log': logs, 'pk': admin.pk, 'notif_list': notif_list,
                   'isadmin': True, 'is_staff': is_staff})


def calendar(request, pk):
    """
    get a calendar for the selected user
    """

    if request.user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()
    owner = get_object_or_404(u_models.User, pk=pk)

    if is_patient(owner):
        user_type = 'patient'
    elif is_doctor(owner):
        user_type = 'doctor'
    elif is_nurse(owner):
        user_type = 'nurse'
    else:  # admin
        user_type = 'admin'

    is_staff = not is_patient(user)

    return render(request, 'healthnet/base_calendar.html',
                  {'pk': pk, 'user': user, 'page_owner': owner,
                   'user_type': user_type, 'notif_list': notif_list,
                   'is_staff': is_staff})


def get_events(request, pk):
    """
    populates the calendar with events, called by base_calendar.js
    :param request: request made
    :param pk: primary key of user
    :return: provides base_calendar with a list of appointments in js format
    """

    curr_user = request.user

    page_user = get_object_or_404(u_models.User, pk=pk)
    page_user = get_user_inst(page_user)
    #  get a list of appointment objects for the current user
    if is_doctor(page_user):
        appointments = list(Appointment.objects.filter(doctor=page_user))

    elif is_patient(page_user):
        appointments = list(Appointment.objects.filter(patient=page_user))

    elif is_nurse(page_user):
        appointments = []
        for doc in get_user_inst(page_user).doctors_list.all():
            appointments += list(Appointment.objects.filter(doctor=doc))

    elif is_admin(page_user):
        appointments = []
        appointments += \
            list(Appointment.objects.filter(hospital=page_user.hospital))

    #  puts appointments into json format
    events = []
    for event in appointments:
        # sets title of appointment based on user
        if is_patient(curr_user) and is_doctor(page_user):
            title = "Appointment"
        elif is_doctor(page_user):
            title = event.patient.__str__()
        elif is_patient(page_user):
            title = event.doctor.__str__()
        else:
            title = " ,".join((event.patient.__str__(),
                               event.doctor.__str__()))
        start = event.date_time.strftime("%Y-%m-%dT%H:%M:%S")
        end = event.get_end().strftime("%Y-%m-%dT%H:%M:%S")
        events.append({'id': event.pk, 'title': title, 'start': start,
                       'end': end})

    return HttpResponse(json.dumps(events),
                        content_type='application/json')


def denied(request):
    """
    for when a user tries to access something that they do not have permissions
    for, sends user to error page
    """

    return render(request, 'healthnet/denied.html')


def page_not_found(request):
    """
    404 page
    """

    return render(request, 'healthnet/404.html')


def time_free(appointment):
    """
    function to determine whether a newly scheduled appointment overlaps
    with an existing one
    :param appointment: the appointment to ve scheduled
    :return: true if the time slot is open
    """
    patient = appointment.patient
    doctor = appointment.doctor

    # creates a list of all appointments for the given patient and doctor
    appointments = list(Appointment.objects.filter(doctor=doctor)) + \
        list(Appointment.objects.filter(patient=patient))

    # loops through all appointments to check that the times don't overlap
    for a in appointments:
        if (appointment.date_time <= a.date_time <= appointment.get_end() or\
                appointment.date_time <= a.get_end() <= appointment.get_end() or
                a.date_time <= appointment.date_time <= a.get_end()) \
                and a.pk != appointment.pk:
            return False
        if appointment.date_time <= datetime.now():
            return False
    return True


def add_appointment(request, pk):
    """
    page for creating an appointment
    """

    if request.user.id is None:
        return redirect('/healthnet/')

    user = request.user
    user = get_user_inst(user)
    notif_list = user.get_notifications()

    if user is None:
        return redirect('/permission_denied/')

    if request.method == "POST":

        form = AppointmentForm(data=request.POST, user=user)
        if form.data['date_time']:
            date_obj = datetime.strptime(form.data['date_time'],
                                         '%b %d %Y, %I:%M %p')
            form.data['date_time'] = \
                datetime.strftime(date_obj, '%Y-%m-%d %H:%M')

        if is_patient(user):
            form.data['duration'] = user.hospital.appointment_length

        if form.is_valid():
            appointment = form.save()
            if appointment.duration < 5:
                appointment.delete()
                return render(request, 'healthnet/form_validation_error.html',
                              {'form_errors':
                                  {'duration':
                                   'Appointments must be 5 minutes or longer'}
                              })
            if appointment.duration > 120:
                appointment.delete()
                return render(request, 'healthnet/form_validation_error.html',
                    {'form_errors':
                        {'duration':
                         'Appointments must be 2 hours or fewer.'}
                    })
            if not time_free(appointment):
                appointment.delete()
                return render(request, 'healthnet/form_validation_error.html',
                              {'form_errors':
                                   {'date_time ': 'This time is not available'}
                               })

            # Generate a log event
            event = ChangelogEntry(
                hospital=appointment.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Appointment between %s and %s Added' %
                            (appointment.doctor.__str__(),
                             appointment.patient.__str__())
            )
            event.save()

            # generate a notification for the doctor
            message = 'Appointment with %s at %s on %s' % \
                      (appointment.patient.first_name + ' ' +
                       appointment.patient.last_name,
                       datetime.strftime(appointment.date_time,
                                         '%I:%M %p'),
                       datetime.strftime(appointment.date_time,
                                         '%m/%d/%Y'))
            notification = Notification(
                receiver=appointment.doctor,
                message=message,
                related_action='/healthnet/edit_appointment/%i/' %
                                appointment.pk
            )
            notification.save()

            return render(request, 'healthnet/appointment_confirmed.html',
                          {'pk': user.pk})
        else:

            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})

    form = AppointmentForm(data=request.POST, user=user)

    # Filter fillable fields
    if is_admin(user):
        return render(request, 'healthnet/add_appointment.html',
                      {'hospital_list': [user.hospital, ],
                       'doctor_list': user.hospital.doctors_list.all(),
                       'patient_list': user.hospital.patients_list.all(),
                       'form': form,
                       'duration': user.hospital.appointment_length,
                       'notif_list': notif_list, 'is_staff': True})

    elif is_doctor(user):
        return render(request, 'healthnet/add_appointment.html',
                      {'hospital_list': user.hospitals_list.all(),
                       'doctor_list': [user, ],
                       'patient_list': user.patients_list.all(),
                       'form': form, 'duration':
                       user.hospitals_list.all()[0].appointment_length,
                       'notif_list': notif_list, 'is_staff': True})

    elif is_nurse(user):
        return render(request, 'healthnet/add_appointment.html',
                      {'hospital_list': [user.hospital, ],
                       'doctor_list': user.doctors_list.all(),
                       'patient_list': user.patients_list,
                       'form': form,
                       'duration': user.hospital.appointment_length,
                       'notif_list': notif_list, 'is_staff': True})

    elif is_patient(user):

        if user.phone and user.address:
            return render(request, 'healthnet/add_appointment.html',
                      {'hospital_list': [user.hospital, ],
                       'doctor_list': [user.dr, ],
                       'patient_list': [user, ],
                       'form': form, 'duration':
                       user.hospital.appointment_length,
                       'notif_list': notif_list, 'is_staff': False})
        else:
            return render(request, 'healthnet/phone_address.html', {"pk": user.pk})


def edit_appointment(request, pk):
    """
    page for editing an appointment
    """

    if request.user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()
    appoint = get_object_or_404(Appointment, pk=pk)

    if request.method == "POST":
        # print post info for debugging
        # print (request.POST)

        form = AppointmentForm(data=request.POST, user=user)
        date_obj = datetime.strptime(form.data['date_time'],
                                     '%b %d %Y, %I:%M %p')
        form.data['date_time'] = \
            datetime.strftime(date_obj, '%Y-%m-%d %H:%M')

        if is_patient(user):
            form.data['duration'] = appoint.duration
        if form.is_valid():
            old_date_time = appoint.date_time
            old_duration = appoint.duration
            if form.cleaned_data['duration'] < 5:
                return render(request, 'healthnet/form_validation_error.html',
                    {'form_errors':
                        {'duration':
                         'Appointments must be 5 minutes or longer'}
                    })
            if form.cleaned_data['duration'] > 120:
                return render(request, 'healthnet/form_validation_error.html',
                    {'form_errors':
                        {'duration':
                         'Appointment duration must be 2 hours or fewer'}
                    })
            appoint.duration = form.cleaned_data['duration']
            appoint.date_time = form.cleaned_data['date_time']

            # if time is taken, revert changes and show error
            if not time_free(appoint):
                appoint.date_time = old_date_time
                appoint.duration = old_duration
                return render(request, 'healthnet/form_validation_error.html',
                              {'form_errors':
                                   {'date_time ': 'This time is not available'}
                               })
            
            appoint.hospital = form.cleaned_data['hospital']
            appoint.note = form.cleaned_data['note']
            appoint.doctor = form.cleaned_data['doctor']
            appoint.patient = form.cleaned_data['patient']
            appoint.save()

            # Generate a log event
            event = ChangelogEntry(
                hospital=appoint.hospital,
                time=datetime.now(),
                generatedby=user,
                description='Appointment %s Edited' % appoint.__str__()
            )
            event.save()

            # generate a notification for the doctor
            message = 'Appointment with %s edited' % \
                (appoint.patient.first_name + ' ' + appoint.patient.last_name)
            notification = Notification(
                receiver=appoint.doctor,
                message=message,
                related_action='healthnet/edit_appointment/%i/' % appoint.pk
            )
            notification.save()

            return render(request, 'healthnet/appointment_confirmed.html',
                          {'pk': user.pk})
        else:
            return render(request, 'healthnet/form_validation_error.html',
                          {'form_errors': form.errors})

    form = AppointmentForm(data=request.POST, user=user,
                           initial={'hospital': appoint.hospital,
                                    'doctor': appoint.doctor,
                                    'patient': appoint.patient,
                                    'duration': appoint.duration})

    # Filter editable information based on who's viewing the page

    if is_admin(user):

        # kick out if hospital is different
        if appoint.hospital.pk != user.hospital.pk:
            return render(request, 'healthnet/denied.html')

        return render(request, 'healthnet/edit_appointment.html',
                      {'appointment': appoint,
                       'hospital_list': [user.hospital, ],
                       'doctor_list': user.hospital.doctors_list.all(),
                       'patient_list': user.hospital.patients_list.all(),
                       'delete_auth': True,
                       'pk': pk, 'form': form, 'duration': 30,
                       'notif_list': notif_list, 'is_staff': True})

    elif is_doctor(user):

        # kick out if doctor is different
        if appoint.doctor.pk != user.pk:
            return render(request, 'healthnet/denied.html')

        return render(request, 'healthnet/edit_appointment.html',
                      {'appointment': appoint,
                       'hospital_list': user.hospitals_list.all(),
                       'doctor_list': [user, ],
                       'patient_list': user.patients_list.all(),
                       'delete_auth': True,
                       'pk': pk, 'form': form, 'duration': 30,
                       'notif_list': notif_list, 'is_staff': True})

    elif is_nurse(user):

        # kick out if doctor is not assigned to nurse
        if appoint.doctor not in user.doctors_list.all():
            return render(request, 'healthnet/denied.html')

        return render(request, 'healthnet/edit_appointment.html',
                      {'appointment': appoint,
                       'hospital_list': [user.hospital, ],
                       'doctor_list': user.doctors_list.all(),
                       'patient_list': user.patients_list,
                       'delete_auth': False,
                       'pk': pk, 'form': form, 'duration': 30,
                       'notif_list': notif_list, 'is_staff': True})

    elif is_patient(user):

        # kick out if user is different
        if appoint.patient.pk != user.pk:
            return render(request, 'healthnet/denied.html')

        return render(request, 'healthnet/edit_appointment.html',
                      {'appointment': appoint,
                       'hospital_list': [user.hospital, ],
                       'doctor_list': [user.dr, ],
                       'patient_list': [user],
                       'delete_auth': True,
                       'pk': pk, 'form': form, 'duration': 30,
                       'notif_list': notif_list, 'is_staff': False})


def delete_appointment(request, pk):
    """
    remove selected appointment
    """
    user = request.user
    if user is None:
        return redirect('healthnet/denied.html')
    appoint = get_object_or_404(Appointment, pk=pk)
    appoint.delete()
    event = ChangelogEntry(
        hospital=appoint.hospital,
        time=datetime.now(),
        generatedby=user,
        description='Appointment %s Removed' % appoint.__str__()
    )
    event.save()

    return redirect('/calendar/' + str(user.pk) + '/')


def stats(request, pk):

    if request.user.id is None:
        return redirect('/healthnet/')

    if int(request.user.pk) != int(pk):
        return render(request, 'healthnet/denied.html')

    if HospitalAdmin.objects.filter(pk=pk).count() != 1:
        return render(request, 'healthnet/404.html')

    user = get_user_inst(request.user)
    notif_list = user.get_notifications()
    hospital = user.hospital

    adm_data = hospital.get_admissions_reason()
    adm_reason = adm_data[0]
    adm_num = adm_data[1]

    prescrip_data = hospital.get_common_prescription()
    prescrip_name = prescrip_data[0]
    prescrip_num = prescrip_data[1]

    is_staff = not is_patient(user)

    # add all prescriptions to a dictionary
    pres_list = {}
    for pres in Prescription.objects.filter(emr__patient__hospital=hospital):
        name = pres.name.upper()
        if name in pres_list.keys():
            pres_list[name] += 1
        else:
            pres_list[name] = 1

    # get top 5 prescriptions
    top_pres = dict(sorted(pres_list.items(), key=operator.itemgetter(1),
                           reverse=True)[:5])

    # save name and count to arrays
    names = ["", "", "", "", ""]
    counts = [0, 0, 0, 0, 0]
    i = 0
    for key, value in top_pres.items():
        names[i] = key
        counts[i] = value
        i += 1

    return render(request, 'healthnet/stats.html', {'hospital': hospital,
                  'users': hospital.get_num_users(),
                  'patients': hospital.get_num_patients(),
                  'doctors': hospital.doctors_list.count(),
                  'per_doc': hospital.get_avg_patients_per_doctor(),
                  'appt_per_pat': hospital.get_avg_patient_visits(),
                  'adm_reason': adm_reason, 'adm_num': adm_num,
                  'prescrip_name': prescrip_name, 'prescrip_num': prescrip_num,
                  'avg_stay_len': hospital.get_avg_stay_len(),
                  'notif_list': notif_list, 'is_staff': is_staff,
                  'pres0name': names[0], 'pres0count': counts[0],
                  'pres1name': names[1], 'pres1count': counts[1],
                  'pres2name': names[2], 'pres2count': counts[2],
                  'pres3name': names[3], 'pres3count': counts[3],
                  'pres4name': names[4], 'pres4count': counts[4]})


def dismiss_notification(request, pk):
    """
    view to dismiss a notification. Doing it without redirecting
    will require ajax
    :return: currently just redirects to user dashboard
    """
    print('made it to py')
    user = request.user
    notification = get_object_or_404(Notification, pk=pk)
    if user.pk == notification.receiver.pk:
        notification.delete()
        return HttpResponse(
            json.dumps({'valid': True, 'delete_id': '#notif_'+pk}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({'valid': False}),
            content_type="application/json"
        )


def send_message(request, pk):
    """
    allows a user to write and send messages in the form of notifications
    """
    user = request.user
    if user.id is None:
        return redirect('/healthnet/')

    user = get_user_inst(user)
    notif_list = user.get_notifications()
    if is_patient(user):
        return redirect("/permission_denied")

    if request.method == 'POST':
        sender = user

        # redirect to failure page if the message is blank
        if request.POST["message"] == "":
            return render(request, 'healthnet/message_failed.html')
        message = request.POST["message"]
        receiver = request.POST["receiver"]

        # create a notification to send to the recipient,
        # related action is a reply
        notification = Notification(
            receiver=u_models.User.objects.get(pk=receiver),
            message='From %s: %s' % (sender, message),
            related_action='/send_message/%i' % user.pk
        )
        notification.save()

        # redirect to a message sent page
        receiver_str = get_user_inst(u_models.User.objects.get(pk=receiver))
        return render(request, 'healthnet/message_sent.html', {
                        'receiver': receiver_str, 'message': message
        })

    if is_patient(u_models.User.objects.get(pk=pk)):
        return redirect("/permission_denied")

    # compile a list of possible recipients
    staff_list = []

    # if this is a reply, default to sending to the original sender
    if int(pk) != int(user.pk):
        staff_list.append(get_user_inst(u_models.User.objects.get(pk=pk)))
        for person in u_models.User.objects.all():
            if (is_admin(person) or is_doctor(person) or is_nurse(person)) and \
                        person.pk != user.pk and int(person.pk) != int(pk):
                staff_list.append(get_user_inst(person))

    # otherwise compile a list of all staff is any order
    else:
        for person in u_models.User.objects.all():
            if (is_admin(person) or is_doctor(person) or is_nurse(person)) and \
                    person.pk != user.pk:
                staff_list.append(get_user_inst(person))

    return render(request, 'healthnet/send_message.html', {
                            'notif_list': notif_list,
                            'staff_list': staff_list,
                            'is_staff': True
    })
