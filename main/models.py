from django.db import models

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=300)
    file = models.FileField(upload_to='files/')

    def __str__(self) -> str:
        return self.name
