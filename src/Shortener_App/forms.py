from django import forms
from .models import JustURL

class ShortUrlForm(forms.ModelForm):
    class Meta:
        model = JustURL
        fields = [
            'input_url',
        ]
