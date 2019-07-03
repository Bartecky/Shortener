from django.shortcuts import render
from django.views import View
from .forms import ShortUrlForm
from .models import JustURL
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
