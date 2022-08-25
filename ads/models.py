from django.db import models

# Create your models here.


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField()


class Category(models.Model):
    name = models.CharField(max_length=100)
