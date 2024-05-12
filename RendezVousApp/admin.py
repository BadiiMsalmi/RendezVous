from django.contrib import admin
from RendezVousApp.models import Patient, Doctor,Appointment, PatientDischarge
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(PatientDischarge)