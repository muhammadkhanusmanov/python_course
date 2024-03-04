from django.urls import path

from ..views import (CreatLesson,SaveFile,GetLessons)

urlpatterns = [
    path('create_lesson/',CreatLesson.as_view()),
    path('save_file/<str:id>',SaveFile.as_view()),
    path('get_lessons/', GetLessons.as_view()),
    path('get_lesson/<str:id>', GetLessons.as_view())
]