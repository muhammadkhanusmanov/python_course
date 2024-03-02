from django.urls import path

from ..views import (CreatLesson,SaveFile)

urlpatterns = [
    path('create_lesson/',CreatLesson.as_view()),
    path('save_task/<str:id>',SaveFile.as_view())
]