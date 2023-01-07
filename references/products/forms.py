from django import forms
from django.forms import inlineformset_factory
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
    slug = forms.CharField(label='URL:', widget=forms.TextInput(attrs={'placeholder': 'URL'}),
                           required=True, max_length=200)


class ImageEditForm(forms.ModelForm):
    class Meta:
        model = ProductImages
        fields = ['image', 'primary']
        image = forms.ImageField(label='Фото:', required=False,
                                 widget=forms.ClearableFileInput(attrs={'id': 'photo'}))
        primary = forms.BooleanField(label='Основное', required='False')

class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ('createdBy', 'createdOn', 'isActive')
    category = forms.ModelChoiceField(label='Категория:', queryset=Categories.objects.all())
    title = forms.CharField(label='Наименование:',
                            widget=forms.TextInput(attrs={'placeholder': 'Наименование', 'size': 50}),
                            required=True, max_length=255,)
    description = forms.CharField(label='Описание:', required=False,
                                  widget=forms.Textarea(attrs={'rows': '3', 'placeholder': 'Описание', 'cols': 52}))
    article = forms.CharField(label='Артикул:', widget=forms.TextInput(attrs={'placeholder': 'Артикул', 'size': 50}),
                              required=False, max_length=16)
    slug = forms.CharField(label='URL:', widget=forms.TextInput(attrs={'placeholder': 'URL', 'size': 50}),
                           required=True, max_length=255)

ImageFormSet = inlineformset_factory(
    Products,
    ProductImages,
    form=ImageEditForm,
    extra=1,
    max_num=6,
    can_delete=True,
    # fk_name=None,
    # fields=('image', 'primary'),
    # fields=None, exclude=None, can_order=False,
    # max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
    )
