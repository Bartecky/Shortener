from django.contrib import admin
from django.urls import re_path
from Shortener_App.views import (
    HomeView,
    CategoryCreateView,
    CategoryListView,
    CustomShortURLCreateView,
    ShortManyURLSView
)

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'^$', HomeView.as_view(), name='home-view'),
    re_path(r'^add/$', CustomShortURLCreateView.as_view(), name='add-custom-url'),
    re_path(r'^many/', ShortManyURLSView.as_view(), name='add-many-urls'),

    re_path(r'^category/add/$', CategoryCreateView.as_view(), name='category-create-view'),
    re_path(r'^categories/$', CategoryListView.as_view(), name='category-list-view'),

]
