from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import ShortUrlForm, JustURLForm, CategoryModelForm, ManyURLSForm
from .models import JustURL, Category
from .utils import create_short_url, token_generator, generate_csv

import re


class HomeView(View):

    def get(self, request, *args, **kwargs):
        form = ShortUrlForm()
        return render(request, 'home.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ShortUrlForm(request.POST or None)
        if form.is_valid():
            url = form.cleaned_data['input_url']
            category = form.cleaned_data['category']
            created = JustURL.objects.create(input_url=url, category=category)
            short_url = create_short_url(created)
            created.short_url = f'{request.get_host()}/{short_url}'
            created.save()
            return render(request, 'short-url-success.html', {'object': created})
        else:
            return render(request, 'home.html', {'form': form})


class CustomShortURLCreateView(View):

    def get(self, request, *args, **kwargs):
        form = JustURLForm()
        return render(request, 'custom-short-url.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = JustURLForm(request.POST or None)
        if form.is_valid():
            url = form.cleaned_data['input_url']
            short_url = form.cleaned_data['short_url']
            category = form.cleaned_data['category']
            if JustURL.objects.filter(short_url__contains=short_url).exists():
                message = 'Token is already in use'
                return render(request, 'custom-short-url.html', {'form': JustURLForm,
                                                                 'message': message})
            created = JustURL.objects.create(input_url=url, short_url=f'{request.get_host()}/{short_url}',
                                             category=category)
            created.save()
            return render(request, 'short-url-success.html', {'object': created})
        else:
            return render(request, 'home.html', {'form': form})


class ShortManyURLSView(View):
    def get(self, request, *args, **kwargs):
        form = ManyURLSForm()
        return render(request, 'short-many-urls.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ManyURLSForm(request.POST or None)
        if form.is_valid():
            urls = form.cleaned_data['input_url']
            urls_list = re.findall(r"[\w.']+", urls)
            data_list = []
            for url in urls_list:
                if not url.startswith('http://') or not url.startswith('www.'):
                    url = 'http://' + url
                if not url.endswith(('.com', '.pl', '.de', '.uk')):
                    url += '.com'
                instance = JustURL.objects.create(input_url=url, short_url=token_generator())
                print(instance.input_url, instance.short_url)
                instance.save()
                data = [instance.input_url, instance.short_url]
                data_list.append(data)
            generate_csv(data_list)
            return render(request, 'short-many-urls.html', {'form': form})

class CategoryCreateView(CreateView):
    template_name = 'category-create-view.html'
    form_class = CategoryModelForm


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'category-list-view.html'
