from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView
from .forms import ShortUrlForm, CategoryModelForm
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
            created = JustURL.objects.create(input_url=url)
            short_url = create_short_url(created)
            created.short_url = f'{request.get_host()}/{short_url}'
            created.save()
        return render(request, 'home.html', {'form': form})


class CategoryCreateView(CreateView):
    template_name = 'category-create-view.html'
    form_class = CategoryModelForm


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'category-list-view.html'
