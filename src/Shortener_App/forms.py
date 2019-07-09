from django import forms
from .models import JustURL, Category
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .utils import check_input_url
from Shortener_Project.settings import SHORTCODE
import re


class ShortUrlForm(forms.ModelForm):
    input_url = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'http://'}))
    category = forms.ModelChoiceField(label='Choose category', queryset=Category.objects.all().order_by('name'),
                                      required=False)

    class Meta:
        model = JustURL
        fields = [
            'input_url',
            'category'
        ]

    def clean_input_url(self):
        url = self.cleaned_data['input_url']
        result = check_input_url(url)
        try:
            URLValidator(result)
        except:
            raise ValidationError('Invalid URL!')
        return result


class JustURLForm(forms.ModelForm):
    input_url = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'http://'}))
    short_url = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'your token here'}),
                                max_length=SHORTCODE, min_length=SHORTCODE)

    class Meta:
        model = JustURL
        fields = [
            'input_url',
            'short_url',
            'category'
        ]

    def clean_short_url(self):
        short_url = self.cleaned_data['short_url']
        if re.match('^[\w\d]+$', short_url):
            return short_url

    def clean_input_url(self):
        url = self.cleaned_data['input_url']
        result = check_input_url(url)
        try:
            URLValidator(result)
        except:
            raise ValidationError('Invalid URL!')
        return result


class ManyURLSForm(forms.ModelForm):
    input_url = forms.CharField(label='', max_length=1024, widget=forms.Textarea(attrs={
        'cols': 40, 'rows': 15,
        'placeholder': 'paste here many links separated by special characters, excluding "." and catch your csv file!'
    }))

    class Meta:
        model = JustURL
        fields = [
            'input_url',
        ]


class JustULRUpdateForm(forms.ModelForm):
    class Meta:
        model = JustURL
        fields = [
            'active',
            'category'
        ]


class CategoryModelForm(forms.ModelForm):
    name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'enter category name'}))
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'cols': 40, 'rows': 15, 'placeholder': 'describe category'
    }))

    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]


class CategoryUpdateModelForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'cols': 40, 'rows': 15, 'placeholder': 'Describe category'
    }))

    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]


class CounterCountingForm(forms.ModelForm):
    class Meta:
        model = JustURL
        fields = []
