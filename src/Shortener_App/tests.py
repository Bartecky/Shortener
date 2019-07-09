from django.test import SimpleTestCase
from django.urls import resolve, reverse
from Shortener_App.views import *



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

