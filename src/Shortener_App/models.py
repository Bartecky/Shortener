from django.db import models

# Create your models here.
class JustURL(models.Model):
    input_url = models.CharField(max_length=256)
    short_url = models.CharField(max_length=24, unique=True, blank=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)


