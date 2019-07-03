from django.db import models
from django.urls import reverse_lazy

# Categories = (
#     ('1', 'Undefined'),
#     ('2', 'IT'),
#     ('3', 'Sport'),
#     ('4', 'Media'),
#     ('5', 'Movies'),
#     ('6', 'Traveling'),
#     ('7', 'Games'),
#     ('8', 'Books'),
#     ('9', 'Social Media'),
#     ('10', 'News')
# )

class JustURL(models.Model):
    input_url = models.CharField(max_length=256)
    short_url = models.CharField(max_length=24, unique=True, blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('home-view')



