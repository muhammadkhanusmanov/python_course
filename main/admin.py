from django.contrib import admin
from .models import (Lesson,Completed)

admin.site.register([
    Lesson, Completed
])



