from django.urls import path

from ..views import (CompletedView,CopUser)

urlpatterns = [
    path('getcompletes/',CompletedView.as_view()),
    path('addcompleted/', CompletedView.as_view()),
    path('comletesuser/',CopUser.as_view())
]