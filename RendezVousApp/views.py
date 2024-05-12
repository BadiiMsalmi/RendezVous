from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import  DoctorSignUpSerializer, PatientSignUpSerializer, UserLoginSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group

@api_view(['POST'])
def patientSignup(request):
    serializer = PatientSignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = request.data.get('user', {}).get('username')
        if username:
            user = User.objects.get(username=username)
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "user": serializer.data,  # Access serializer data after validation
                "token": token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Username not provided in request data."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def doctorSignup(request):
    serializer = DoctorSignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        username = request.data.get('user', {}).get('username')
        if username:
            user = User.objects.get(username=username)
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "user": serializer.data,  # Access serializer data after validation
                "token": token.key
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Username not provided in request data."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def signIn(request):
    data = request.data
    serializer = UserLoginSerializer(data=data)
    if serializer.is_valid():
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            token, created_token = Token.objects.get_or_create(user=user)
            user_group = None
            if user.groups.exists():
                user_group = user.groups.first().name
            response_data = {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,  # Add any other fields you need
                    "group": user_group  # Add user group to the response
                },
                "token": token.key
            }
            return Response(response_data, status=status.HTTP_200_OK)
    return Response({"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def testview(request):
    return Response({"message":"testview page"})

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message":"Logged out successfully"})

