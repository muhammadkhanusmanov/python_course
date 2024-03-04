from django.db import models
from django.contrib.auth.models import User

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=300)
    file = models.FileField(upload_to='files/')

    def __str__(self) -> str:
        return self.name
    
class Completed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.user.username
