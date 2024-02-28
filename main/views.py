from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.http import HttpRequest,JsonResponse,FileResponse
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class Signup(APIView):
    
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password'],
    ),
    responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Status': openapi.Schema(type=openapi.TYPE_STRING),
                    'Token': openapi.Schema(type=openapi.TYPE_STRING),
                })
            },
    operation_description="Create a new user with the provided username, password, and optional first name.",
    )
    def post(self, request):
        data = request.data
        username = data.get('username',None)
        password = data.get('password',None)
        first_name = data.get('first_name',username)
        if username is not None and first_name is not None:
            try:
                user = User.objects.get(username=username)
                return Response({'Status':'This username is already'},status=status.HTTP_208_ALREADY_REPORTED)
            except:
                user = User.objects.create(
                    username=username,
                    password=make_password(password),
                    first_name=first_name
                )
                user.save()
                token = Token.objects.create(user=user)
                return Response({'Status':'created','Token':token.key},status=status.HTTP_201_CREATED)
        return Response({'Status':'BAD_REQUEST'},status=status.HTTP_400_BAD_REQUEST)
    

class Signin(APIView):
    authentication_classes = [BasicAuthentication]
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username by Basic Authentication'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password by Basic Authentication'),
        }
    ),
    responses={
        200: openapi.Schema(type=openapi.TYPE_STRING),
        401: openapi.Schema(type=openapi.TYPE_STRING),
    },
    operation_description="Get information about the authenticated user.",
    security=[{"basic": []}],  # Specify Basic Authentication
    )

    
    def post(self,request):
        user = request.user
        try:
            token,created = Token.objects.get_or_create(user = user)
            return Response({'Status': 'OK','Token': token.key},status=status.HTTP_200_OK)
        except:
            return Response({'Status': 'User not found', 'Token':None},status=status.HTTP_404_NOT_FOUND)
        


class Logout(APIView):
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        request_body=None,
        responses={
            200: openapi.Schema(type=openapi.TYPE_BOOLEAN),
            400: openapi.Schema(type=openapi.TYPE_BOOLEAN),
        },
        operation_description="Send a token to delete the user's token",
        security=[{"token": []}], 
        manual_parameters=[
        openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Token 633ae0c6603495498d6f121ed984645dd1223135')
        ],
    )

    def delete(self, request):
        user = request.user
        try:
            token = Token.objects.get(user=user)
            token.delete()
            return Response({'status':True},status=status.HTTP_204_OK)
        except:
            return Response({'status':False},status=status.HTTP_400_BAD_REQUEST)