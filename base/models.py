from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections", default=1)  # default=1, якщо користувач з ID 1 має бути власником за замовчуванням

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title
