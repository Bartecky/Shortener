from django import forms
from .models import JustURL, Category


class ShortUrlForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = JustURL
        fields = [
            'input_url',
            'category'
        ]


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

