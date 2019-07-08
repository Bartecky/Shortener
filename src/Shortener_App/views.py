from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import ShortUrlForm, JustURLForm, CategoryModelForm, ManyURLSForm, JustULRUpdateForm, \
    CategoryUpdateModelForm, CounterCountingForm
from .models import JustURL, Category, ClickTracking
from .utils import create_short_url, token_generator, generate_csv, get_client_ip
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
            if request.user.is_superuser:
                return redirect(reverse('url-detail-view', kwargs={'pk': created.pk}))
            return redirect(reverse('success-url-view', kwargs={'pk': created.pk}))
        return render(request, 'home.html', {'form': form})


class SuccessUrlView(View):
    def get(self, request, pk, *args, **kwargs):
        object = JustURL.objects.get(pk=pk)
        form = CounterCountingForm()
        return render(request, 'success-url-view.html', {'object': object,
                                                         'form': form})

    def post(self, request, pk, *args, **kwargs):
        object = JustURL.objects.get(pk=pk)
        form = CounterCountingForm(request.POST or None)
        if form.is_valid():
            object.count += 1
            ip = get_client_ip(request)
            client_agent = request.META['HTTP_USER_AGENT']
            clicktracker = ClickTracking.objects.create(
                client_ip = ip,
                user_agent = client_agent,
            )
            clicktracker.url.add(object)
            clicktracker.save()
            object.save()
            return link_redirect(request, pk)
        return redirect('home-view')


class URLDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        form = CounterCountingForm()
        object = JustURL.objects.get(pk=pk)
        return render(request, 'url-detail-view.html', {'object': object,
                                                        'form': form})

    def post(self, request, pk, *args, **kwargs):
        object = JustURL.objects.get(pk=pk)
        form = CounterCountingForm(request.POST or None)
        if form.is_valid():
            object.count += 1
            ip = get_client_ip(request)
            client_agent = request.META['HTTP_USER_AGENT']
            clicktracker = ClickTracking.objects.create(
                client_ip=ip,
                user_agent=client_agent,
            )
            clicktracker.url.add(object)
            clicktracker.save()
            object.save()
            return link_redirect(request, pk)
        return render(request, 'url-detail-view.html', {'object': object,
                                                        'form': form})


class URLUpdateView(UpdateView):
    queryset = JustURL.objects.all()
    form_class = JustULRUpdateForm
    template_name = 'url-update-view.html'


class URLDeleteView(DeleteView):
    model = JustURL
    template_name = 'url-delete-view.html'
    success_url = reverse_lazy('home-view')


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
            if request.user.is_superuser:
                return redirect(reverse('url-detail-view', kwargs={'pk': created.pk}))
            return redirect(reverse('success-url-view', kwargs={'pk': created.pk}))
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
        return render(request, 'home.html', {'form': ShortUrlForm,
                                             'message': 'Success! Saved data to file.'})


class CategoryCreateView(CreateView):
    template_name = 'category-create-view.html'
    form_class = CategoryModelForm


class CategoryListView(ListView):
    queryset = Category.objects.all()
    template_name = 'category-list-view.html'


class CategoryDetailView(DetailView):
    queryset = Category.objects.all()
    template_name = 'category-detail-view.html'


class CategoryUpdateView(UpdateView):
    queryset = Category.objects.all()
    form_class = CategoryUpdateModelForm
    template_name = 'category-update-view.html'
    success_url = reverse_lazy('category-list-view')


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category-delete-view.html'
    success_url = reverse_lazy('category-list-view')


def link_redirect(request, pk):
    instance = get_object_or_404(JustURL, pk=pk)
    return redirect(instance.input_url)


