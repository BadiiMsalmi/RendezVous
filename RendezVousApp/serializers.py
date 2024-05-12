from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from RendezVousApp.models import Doctor, Patient
from rest_framework import serializers

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','password')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

class PatientSignUpSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Patient
        fields = ('user','Patient_First_Name', 'Patient_Last_Name', 'gender', 'contact', 'address')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user , **validated_data)
        # Create a token for the patient
        Token.objects.create(user=user)
        return patient




class DoctorSignUpSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = ('user','Doctor_First_Name','Doctor_Last_Name','gender', 'contact', 'address', 'department')
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user , **validated_data)
        # Create a token for the doctor
        Token.objects.create(user=user)
        return doctor