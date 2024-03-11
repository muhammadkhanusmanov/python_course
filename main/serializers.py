from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from .models import Lesson,Completed
from django.contrib.auth.models import User


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'url', 'file']

    def create(self, validated_data):
        file = validated_data.pop('file')
        lesson = Lesson.objects.create(file=file, **validated_data)
        return lesson


class ComleteSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True)
    class Meta:
        model = Completed
        fields = ['id', 'user','lessons']
        

class UserSerializer(ModelSerializer):
    completed = ComleteSerializer(many=True)
    class Meta:
        model = User
        fields = ['id','username', 'first_name','completed']