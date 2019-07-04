from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import ShortUrlForm, JustURLForm, CategoryModelForm
from .models import JustURL, Category
from .utils import create_short_url


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
                message = 'token is already in use or isn\'t valid'
                return render(request, 'custom-short-url.html', {'form': ShortUrlForm,
                                                                 'message': message})
            created = JustURL.objects.create(input_url=url, short_url=f'{request.get_host()}/{short_url}', category=category)
            created.save()
            return render(request, 'short-url-success.html', {'object': created})
        else:
            return render(request, 'home.html', {'form': form})


class CategoryCreateView(CreateView):
    template_name = 'category-create-view.html'
    form_class = CategoryModelForm


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'category-list-view.html'
