from rest_framework.serializers import ModelSerializer, SerializerMethodField, ReadOnlyField
from .models import Lesson,Completed

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
    username = ReadOnlyField(source='user.username')
    class Meta:
        model = Completed
        fields = ['id', 'user', 'username','lessons']
