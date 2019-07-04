from django import forms
from .models import JustURL, Category
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re

class ShortUrlForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = JustURL
        fields = [
            'input_url',
            'category'
        ]

    def clean_input_url(self):
        url = self.cleaned_data['input_url']
        if url.startswith('http://') or url.startswith('www.'):
            result = url
        else:
            result = 'http://' + url

        if not url.endswith(('.com', '.pl', '.de', '.uk')):
            result += '.com'
        try:
            URLValidator(result)
        except:
            raise ValidationError('Invalid URL!')
        return result


class JustURLForm(forms.ModelForm):
    short_url = forms.CharField(max_length=8, min_length=8)

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
        if url.startswith('http://') or url.startswith('www.'):
            result = url
        else:
            result = 'http://' + url

        if not url.endswith(('.com', '.pl', '.de', '.uk')):
            result += '.com'
        try:
            URLValidator(result)
        except:
            raise ValidationError('Invalid URL!')
        return result


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name',
            'description'
        ]
        required = (
            'name'
        )
        widgets = {
            'description': forms.Textarea(attrs={'cols': 40, 'rows': 15},
                                          ),
        }
