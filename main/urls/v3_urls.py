from django.urls import path

from ..views import (CompletedView)

urlpatterns = [
    path('addcompleted/', CompletedView.as_view()),
]