from django.urls import path

from ..views import (CompletedView)

urlpatterns = [
    path('getcompletes/',CompletedView.as_view()),
    path('addcompleted/', CompletedView.as_view()),
]