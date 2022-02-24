from django.db import models


class Record(models.Model):
    user_id = models.IntegerField(blank=False)
    data = models.BinaryField()
    state = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)
