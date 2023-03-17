# countries/models.py
from django.db import models

class Document(models.Model):
    id = models.CharField(max_length = 180, primary_key=True)
    title = models.CharField(max_length = 200)
    price = models.CharField(max_length = 200)

    def __str__(self):
        return self.task