from django.contrib import admin
from .models import JustURL, Category, ClickTracking

admin.site.register(JustURL)
admin.site.register(Category)
admin.site.register(ClickTracking)