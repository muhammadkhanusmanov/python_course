from django.urls import path

from ..views import (Signup,Signin,Logout)

urlpatterns = [
    path('signup/',Signup.as_view()),
    path('signin/',Signin.as_view()),
    path('logout/',Logout.as_view()),
]