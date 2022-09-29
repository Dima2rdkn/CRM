from django import forms
from .models import Stores

class StoreEditForm(forms.ModelForm):
    class Meta:
        model = Stores
        fields = ['name', 'slug']
    name = forms.CharField(label='Склад:', widget=forms.TextInput(attrs={'placeholder': 'Склад'}),
                           required=True, max_length=100)
    slug = forms.CharField(label='Ярлык:', widget=forms.TextInput(attrs={'placeholder': 'Ярлык'}),
                           required=True, max_length=200)
