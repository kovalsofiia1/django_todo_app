
# Create your models here.
# base/models.py
from django.db import models

class Collection(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    deadline = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
