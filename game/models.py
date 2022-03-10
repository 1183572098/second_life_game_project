from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PHONE_NO_MAX_LENGTH = 20
    phone_no = models.CharField(max_length=PHONE_NO_MAX_LENGTH)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    TITLE_MAX_LENGTH = 100
    title = models.CharField(max_length=TITLE_MAX_LENGTH, blank=False)
    CONTENT_MAX_LENGTH = 500
    content = models.CharField(max_length=CONTENT_MAX_LENGTH)
    upperID = models.IntegerField(blank=False, default=-1)
    is_del = models.BooleanField(default=False)


class Announcement(models.Model):
    TITLE_MAX_LENGTH = 100
    title = models.CharField(max_length=TITLE_MAX_LENGTH, blank=False)
    CONTENT_MAX_LENGTH = 500
    content = models.CharField(max_length=CONTENT_MAX_LENGTH, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Record(models.Model):
    user_id = models.IntegerField(blank=False)
    data = models.BinaryField()
    state = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)
    location = models.IntegerField(blank=False)
