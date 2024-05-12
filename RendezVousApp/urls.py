from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.signIn),
    path('patientsignup/',views.patientSignup),
    path('doctorsignup/',views.doctorSignup),
    path('testView/',views.testview),
    path('logout/',views.logout)
]
