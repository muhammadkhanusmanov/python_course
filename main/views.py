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

from .serializers import LessonSerializer,ComleteSerializer

from .models import Lesson, Completed

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
            if user.is_superuser:
                return Response({'Status': 'Admin','Token': token.key},status=status.HTTP_200_OK)
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
            return Response({'status':True},status=status.HTTP_200_OK)
        except:
            return Response({'status':False},status=status.HTTP_400_BAD_REQUEST)
    

class GetUsers(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        urs = []
        for user in users:
            ur = {
                'username':user.username,
                'first_name':user.get('first_name','Noname')
            }
            urs.append(ur)
        return Response(urs)

class CreatLesson(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    # parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'url': openapi.Schema(type=openapi.TYPE_STRING),
            'file': openapi.Schema(type=openapi.TYPE_FILE),
        },
        required=['name', 'url','file'],
    ),
        responses={
            201: openapi.Schema(type=openapi.TYPE_BOOLEAN),
            400: openapi.Schema(type=openapi.TYPE_BOOLEAN),
        },
        operation_description="send properties for creating a new lesson",
        security=[{"token": []}], 
        manual_parameters=[
        openapi.Parameter('Authorization', in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, description='Token 633ae0c6603495498d6f121ed984645dd1223135')
        ],
    )

    def post(self, request):
        data = request.data
        try:
            file = file = request.FILES.get('file')

            lesson = Lesson.objects.create(
                name = data['name'],
                url = data['url'],
                file = file
            )
            lesson.save()

            return Response({'Status':'Created'},status=status.HTTP_201_CREATED)
        except:
             return Response({'Status':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)
        
class SaveFile(APIView):
    def get(self, request, id: str):
        try:
            file = Lesson.objects.get(id=id)
            file = file.file
            rs = open(file.path,'rb')
            return FileResponse(rs)
        except:
            return Response({'status': False},status=status.HTTP_400_BAD_REQUEST)
        
class GetLessons(APIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAdminUser]

    def post(self, request):
        lessons = Lesson.objects.all()
        lns = []
        for lesson in lessons:
            lesson = LessonSerializer(lesson).data
            lesson['file'] = f"https://pycourse.pythonanywhere.com/v2/save_file/{lesson['id']}"
            lns.append(lesson)
        return Response(lns)
    
    def get(self,request, id:str):
        try:
            lesson = Lesson.objects.get(id=id)
            lesson = LessonSerializer(lesson).data
            lesson['file'] = f"https://pycourse.pythonanywhere.com/v2/save_file/{lesson['id']}"
            return Response(lesson)
        except:
            return Response({'status':'Bad Request'},status=status.HTTP_400_BAD_REQUEST)

class CompletedView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        user_instance = request.user
        lesson_id = request.data.get('lesson')

        try:
            completed_instance = Completed.objects.get(user=user_instance)
            lesson_instance = Lesson.objects.get(id=lesson_id)
            completed_instance.lessons.add(lesson_instance)
            completed_instance.save()
            return Response({'status': True}, status=status.HTTP_200_OK)
        except Completed.DoesNotExist:
            # Agar Completed obyekti mavjud emas bo'lsa
            completed_instance = Completed.objects.create(user=user_instance)
            lesson_instance = Lesson.objects.get(id=lesson_id)
            completed_instance.lessons.add(lesson_instance)
            return Response({'status': True}, status=status.HTTP_200_OK)
    def get(self,request):
        cmpts=Completed.objects.all()
        srl = ComleteSerializer(cmpts,many=True)
        return Response(srl.data)