from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Record(models.Model):
    user_id = models.IntegerField(blank=False)
    data = models.BinaryField()
    state = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)
