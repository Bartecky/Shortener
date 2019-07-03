from django.db import models

# Create your models here.
class JustURL(models.Model):
    input_url = models.CharField(max_length=200)

