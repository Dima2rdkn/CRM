from django import forms
from django.forms import formset_factory
from .models import Categories, Products, ProductImages, Specifications, Feedback

class CatEditForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name', 'parent', 'slug', 'image']

    parent = forms.ModelChoiceField(label='Группа:',  required=False, queryset=Categories.objects.all())
    image = forms.ImageField(label='Картинка:', required=False,
                             widget=forms.ClearableFileInput(attrs={'id': 'avatar'}))
    name = forms.CharField(label='Категория:', widget=forms.TextInput(attrs={'placeholder': 'Категория'}),
                           required=True, max_length=100)
    slug = forms.CharField(label='Ярлык:', widget=forms.TextInput(attrs={'placeholder': 'Ярлык'}),
                           required=True, max_length=200)


class ImageEditForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image', 'primary']


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['category', 'title', 'slug', 'article', 'description']


