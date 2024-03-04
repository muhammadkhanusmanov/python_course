from django.urls import path

from ..views import (Signup,Signin,Logout,GetUsers)

urlpatterns = [
    path('signup/',Signup.as_view()),
    path('signin/',Signin.as_view()),
    path('logout/',Logout.as_view()),
    path('getusers/',GetUsers.as_view()),
]