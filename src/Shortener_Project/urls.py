from django.contrib import admin
from django.urls import re_path
from Shortener_App.views import (
    HomeView,
    CustomShortURLCreateView,
    ShortManyURLSView,
    URLDetailView,
    URLUpdateView,
    URLDeleteView,
    CategoryCreateView,
    CategoryListView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
)

urlpatterns = [
    re_path(r'admin/', admin.site.urls),
    re_path(r'^$', HomeView.as_view(), name='home-view'),
    re_path(r'^add/$', CustomShortURLCreateView.as_view(), name='add-custom-url'),
    re_path(r'^add-many/', ShortManyURLSView.as_view(), name='add-many-urls'),
    re_path(r'^detail/(?P<pk>(\d)+)/$', URLDetailView.as_view(), name='url-detail-view'),
    re_path(r'^update/(?P<pk>(\d)+)/$', URLUpdateView.as_view(), name='url-update-view'),
    re_path(r'^delete/(?P<pk>(\d)+)/$', URLDeleteView.as_view(), name='url-delete-view'),

    re_path(r'^category/add/$', CategoryCreateView.as_view(), name='category-create-view'),
    re_path(r'^categories/$', CategoryListView.as_view(), name='category-list-view'),
    re_path(r'^detail/category/(?P<pk>(\d)+)/$', CategoryDetailView.as_view(), name='category-detail-view'),
    re_path(r'^update/category/(?P<pk>(\d)+)/$', CategoryUpdateView.as_view(), name='category-update-view'),
    re_path(r'^delete/category/(?P<pk>(\d)+)/$', CategoryDeleteView.as_view(), name='category-delete-view'),

]
