from django import forms
from .models import Measure

class MeasureEditForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = ['name', 'description', 'slug']
    name = forms.CharField(label='Условное:', widget=forms.TextInput(attrs={'placeholder': 'усл.'}),
                           required=True, max_length=8)
    description = forms.CharField(label='Описание:', widget=forms.TextInput(attrs={'placeholder': 'Описание'}),
                                  required=True, max_length=128)
    slug = forms.CharField(label='Ярлык:', widget=forms.TextInput(attrs={'placeholder': 'Ярлык'}),
                           required=True, max_length=8)
