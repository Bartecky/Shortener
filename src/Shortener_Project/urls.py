from django.contrib import admin
from django.urls import re_path
from Shortener_App.views import HomeView

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'', HomeView.as_view(), name='home-view')
]
