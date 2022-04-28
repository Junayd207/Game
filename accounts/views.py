from django.http import HttpResponse
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import FeedbackSerializer

@api_view(['POST'])
def sign_up(request):
    data = request.data
    email = data['email']
    username = data['username']
    password = data['password']
    if (email == '' or username == '' or password == ''):
        return Response('empty-field', status.HTTP_400_BAD_REQUEST)
    if (User.objects.filter(email=email).exists()):
        return Response('email-exists', status.HTTP_400_BAD_REQUEST)
    if (User.objects.filter(username=username).exists()):
        return Response('username-exists', status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    return Response((), status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    data = request.data
    username = data['username']
    password = data['password']
    try:
        user = User.objects.get(username=username)
        email = user.email
        serializer = UserSerializer(instance = user, data = {'username':username,'email':email,'password':password})

        if serializer.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return Response(serializer.data, status= status.HTTP_200_OK)

    except:
        return Response((), status = status.HTTP_404_NOT_FOUND)                   

    return Response(serializer.data, status = status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def store_contact_message(request):
    data = request.data
    serializer = FeedbackSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(None, status=status.HTTP_400_BAD_REQUEST)




