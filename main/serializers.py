from rest_framework.serializers import ModelSerializer
from .models import Lesson

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'url', 'file']

    def create(self, validated_data):
        file = validated_data.pop('file')
        lesson = Lesson.objects.create(file=file, **validated_data)
        return lesson