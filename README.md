# HealthNet 

This was a 2nd year class project meant to simulate the development of a real healthcare system from requirements to deployment.

__Original customer README below:__

"Your Online Healthcare Management System"

Table of Contents:

 I. [Installation](https://github.com/BenAlderfer/Healthnet#section-i-installation)
  
 II. [Operation](https://github.com/BenAlderfer/Healthnet#section-ii-operation)
 
 III. [Bugs and Disclaimers](https://github.com/BenAlderfer/Healthnet#section-iii-bugs-and-disclaimers)
 
 IV. [Pending Features](https://github.com/BenAlderfer/Healthnet#section-iv-pending-features)
 
 V. [Development Credits](https://github.com/BenAlderfer/Healthnet#section-v-development-credits)
  
 VI. [Appendix](https://github.com/BenAlderfer/Healthnet#section-vi-appendix)


## Section I: Installation

Extract the contents of this .zip archive to the directory from which you wish
to run your new HealthNet server.

No further operation is necessary to complete installation.

For testing purposes, a simple skeleton database is provided with limited
hospitals and staff. For more complete testing, double-click on add_records.bat
and enter the names of the provided .CSV files (doctors.csv, nurses.csv,
patients.csv, emr.csv) when prompted.

## Section II: Operation

__Running HealthNet__

All server operations are conducted from the /healthnetproject directory.

To execute the server, double-click on "run.bat". It can then be viewed in any
web browser at the address "localhost:8000".

Superuser accounts can be created by double-clicking on "createsuperuser.bat".
Superusers should access the administrator interface at "localhost:8000/admin/".

In the event that the system database (healthnet.db) is deleted, it can be
recreated by double-clicking on "remake_db.bat", though all information will still
be lost.

----------

__User Accounts__

Users may be registered at localhost:8000/users/register_patient/ and /register_staff/
All doctor and nurse accounts must be approved by the hospital's administrator,
and hospital administrator accounts must be approved by a superuser.

Once users have registered, they may login to the system using their email
address and selected password.

All users must select a hospital when they are registered. Only the system
administrators may create entries for hospitals.

For data integrity reasons, if users are to be removed from the system, a system
administrator should deactivate their accounts instead of deleting them. This
prevents any possible issues based on missing database dependencies.

----------

__In This Package__

Accounts included with the default database are as follows:

### Superuser

username:   admin

password:   apple.123

----------

### Hospital Administrators

Name:       Mark Greene

Username:   greene@health.net

Password:   apple.123

Hospital:   County General Hospital

----------

Name:       Richard Webber

Username:   webber@health.net

Password:   apple.123

Hospital:   Grey-Sloan Memorial Hospital

These are all the users initially required to operate HealthNet
If the option to load additional records from the provided .csv files was
chosen during installation, multiple other users will appear in the system.

----------

### Doctors

Name:       Meredith Grey

Username:   grey@health.net

Password:   apple.123

Hospitals:  Grey-Sloan Memorial Hospital

----------

Name:       Doug Ross

Username:   ross@health.net

Password:   apple.123

Hospitals:  County General Hospital

----------

Name:       Gregory House

Username:   house@health.net

Password:   apple.123

Hospitals:  Grey-Sloan Memorial Hospital, County General Hospital

----------

### Nurses

Name:       Carol Hathaway

Username:   hathaway@health.net

Password:   apple.123

Hospital:   County General Hospital

Doctors:    Meredith Grey, Gregory House

----------

Name:       Samantha Taggart

Username:   taggart@health.net

Password:   apple.123

Hospital:   County General Hospital

Doctors:    Meredith Grey

Name:       Olivia Harper

----------

Username:   harper@health.net

Password:   apple.123

Hospital:   Grey-Sloan Memorial Hospital

Doctors:    None

### Patients

Name:       Charlie Abbott

Username:   abbott@health.net

Password:   apple.123

Hospital:   Grey-Sloan Memorial Hospital

Doctor:     Meredith Grey

----------

Name:       Ruth Bennett

Username:   bennett@health.net

Password:   apple.123

Hospital:   Grey-Sloan Memorial Hospital

Doctor:     Gregory House

Notes:      This patient is initially missing some contact information and
            will be required to add it before scheduling any appointments.
            
----------

Name:       Carla Reece

Username:   reece@health.net

Password:   apple.123

Hospital:   County General Hospital

Doctor:     Gregory House

----------

Name:       Al Boulet

Username:   boulet@health.net

Password:   apple.123

Hospital:   County General Hospital

Doctor:     Doug Ross

In addition, a number of medical records will have been added for each patient.

## Section III: Bugs and Disclaimers

Bugs:

*   No server bugs are known to exist at this time. If any bugs are uncovered,
    please send a bug report to Tessa Nijssen.

Disclaimers:

*   The messaging system does not allow for filtering recipient by hospital;
    instead, a full staff listing is provided.

*   During profile registration and updating, certain errors (duplicate
    account, etc.) are not reported until form submission


## Section IV: Pending Features

All system functionality has been implemented.

## Section V: Development Credits

#### Jonathan Kleinfeld
Team Coordinator

#### John Murray
Quality Assurance Coordinator

#### John Byrne
Testing Coordinator

#### Ben Alderfer
Design and Development Coordinator

#### Tessa Nijssen
Requirements Coordinator

## Section VI: Appendix

Documents contained in /~f261-04d/Release-2/ are as follows:

Requirements document:   Requirements-HealthNet.pdf

Design document:         Design.pdf

Test plan spreadsheet:   TestPlanTracker.xlsx

Readme:                  README.txt

Project source package:  Healthnet.zip

Project installer file:  HealthNet-Turnkey.bat

Command-line utility:    unzip.exe

We hope you find HealthNet both useful and enjoyable. Feel free to contact
any of the staff listed above with questions or comments.
