from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.FileField()
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    liked_events = models.ManyToManyField(Event)

    def __str__(self):
        return self.user.username