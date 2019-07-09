from django.test import SimpleTestCase, TestCase, Client
from django.urls import resolve, reverse
from Shortener_App.models import JustURL, Category, ClickTracking
from Shortener_App.views import *
from django.contrib.auth.models import User
import json


class TestUrls(SimpleTestCase):

    def test_home_view_url_resolves(self):
        url = reverse('home-view')
        self.assertEquals(resolve(url).func.view_class, HomeView)

    def test_success_url_resolves(self):
        url = reverse('success-url-view', args=['77'])
        self.assertEquals(resolve(url).func.view_class, SuccessUrlView)

    def test_add_custom_url_resolves(self):
        url = reverse('add-custom-url')
        self.assertEquals(resolve(url).func.view_class, CustomShortURLCreateView)

    def test_add_many_url_resolves(self):
        url = reverse('add-many-urls')
        self.assertEquals(resolve(url).func.view_class, ShortManyURLSView)

    def test_detail_view_url_resolves(self):
        url = reverse('url-detail-view', args=['77'])
        self.assertEquals(resolve(url).func.view_class, URLDetailView)

    def test_update_url_resolves(self):
        url = reverse('url-update-view', args=['77'])
        self.assertEquals(resolve(url).func.view_class, URLUpdateView)

    def test_delete_url_resolves(self):
        url = reverse('url-delete-view', args=['77'])
        self.assertEquals(resolve(url).func.view_class, URLDeleteView)

    def test_category_create_url_resolves(self):
        url = reverse('category-create-view')
        self.assertEquals(resolve(url).func.view_class, CategoryCreateView)

    def test_category_list_url_resolves(self):
        url = reverse('category-list-view')
        self.assertEquals(resolve(url).func.view_class, CategoryListView)

    def test_category_detail_url_resolves(self):
        url = reverse('category-detail-view', args=['5'])
        self.assertEquals(resolve(url).func.view_class, CategoryDetailView)

    def test_category_update_url_resolves(self):
        url = reverse('category-update-view', args=['5'])
        self.assertEquals(resolve(url).func.view_class, CategoryUpdateView)

    def test_category_delete_url_resolves(self):
        url = reverse('category-delete-view', args=['5'])
        self.assertEquals(resolve(url).func.view_class, CategoryDeleteView)

    def test_clicktracking_detail_url_resolves(self):
        url = reverse('clicktracking-detail-view', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ClickTrackingDetailView)


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = JustURL.objects.create(input_url='http://python.org')
        self.url.short_url = 'X9X9'

        self.category = Category.objects.create(name='Cat1')
        self.url.category = self.category

        self.tracker = ClickTracking.objects.create(client_ip='127.0.0.1', user_agent='Fozilla Mirefox')
        self.tracker.url.add(self.url)

        self.user = User.objects.create_superuser('imsuperuser', '', 'qwerty')
        self.client.force_login(self.user)

    def test_homeview_GET(self):
        response = self.client.get(reverse('home-view'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_homeview_POST(self):
        response = self.client.post(reverse('success-url-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(JustURL.objects.all().count(), 1)

    def test_success_GET(self):
        response = self.client.get(reverse('success-url-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 200)

    def test_success_POST(self):
        response = self.client.post(reverse('url-redirect-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 302)

    def test_url_detail_GET(self):
        response = self.client.get(reverse('url-detail-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 200)

    def test_url_detail_POST(self):
        response = self.client.post(reverse('url-redirect-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 302)

    def test_url_update_GET(self):
        response = self.client.get(reverse('url-update-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 200)

    def test_url_update_POST(self):
        response = self.client.post(reverse('url-update-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 302)

    def test_url_delete_GET(self):
        response = self.client.get(reverse('url-delete-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 200)

    def test_url_delete_POST(self):
        response = self.client.post(reverse('url-delete-view', args=[self.url.pk]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(JustURL.objects.all().count(), 0)

    def test_short_many_urls_GET(self):
        response = self.client.get(reverse('add-many-urls'))
        self.assertEquals(response.status_code, 200)

    def test_short_many_urls_POST(self):
        response = self.client.post(reverse('add-many-urls'))
        self.assertEquals(response.status_code, 302)

    def test_category_create_GET(self):
        response = self.client.get(reverse('category-create-view'))
        self.assertEquals(response.status_code, 200)

    def test_category_create_POST(self):
        response = self.client.post(reverse('category-create-view'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Category.objects.all().count(), 1)

    def test_category_list_GET(self):
        response = self.client.get(reverse('category-list-view'))
        self.assertEquals(response.status_code, 200)

    def test_category_detail_GET(self):
        response = self.client.get(reverse('category-detail-view', args=[self.category.pk]))
        self.assertEquals(response.status_code, 200)

    def test_category_update_GET(self):
        response = self.client.get(reverse('category-update-view', args=[self.category.pk]))
        self.assertEquals(response.status_code, 200)

    def test_category_update_POST(self):
        response = self.client.post(reverse('category-update-view', args=[self.category.pk]))
        self.assertEquals(response.status_code, 200)

    def test_category_delete_GET(self):
        response = self.client.get(reverse('category-delete-view', args=[self.category.pk]))
        self.assertEquals(response.status_code, 200)

    def test_category_delete_POST(self):
        response = self.client.post(reverse('category-delete-view', args=[self.category.pk]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(Category.objects.all().count(), 0)

    def test_tracker_detail_GET(self):
        response = self.client.get(reverse('clicktracking-detail-view', args=[self.tracker.pk]))
        self.assertEquals(response.status_code, 200)

    def tearDown(self):
        del self.client
        del self.url
        del self.category
        del self.tracker
        del self.user
