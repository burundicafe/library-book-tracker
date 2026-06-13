from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100, blank=True, default="")
    year_published = models.IntegerField(null = False, blank = False)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.title