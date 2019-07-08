from django.db import models
from django.urls import reverse_lazy


class JustURL(models.Model):
    input_url = models.CharField(max_length=256)
    short_url = models.CharField(max_length=24, unique=True, blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.input_url} - {self.short_url}'

    def get_absolute_url(self):
        return reverse_lazy('url-detail-view', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('category-detail-view', kwargs={'pk': self.pk})


class ClickTracking(models.Model):
    url = models.ManyToManyField(JustURL)
    client_ip = models.CharField(max_length=16)
    user_agent = models.CharField(max_length=128)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.timestamp} - {self.url}'