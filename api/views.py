from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def register_user(request):
    print("DEBUG DATA:", request.data)

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide username and password'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username': user.username})
    

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
