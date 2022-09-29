from django import forms
from .models import SupplierGroup, Supplier

class GroupEditForm(forms.ModelForm):
    class Meta:
        model = SupplierGroup
        fields = ['parent', 'title', 'description']


class SupplierEditForm(forms.ModelForm):
    class Meta:
        model = Supplier
        exclude = ('createdBy', 'createdOn', 'isActive')

    category = forms.ModelChoiceField(label='Группа:', queryset=SupplierGroup.objects.all())

    name = forms.CharField(label='Наименование:', widget=forms.TextInput(attrs={'placeholder': 'Наименование'}),
                                 required=True, max_length=125)
    full_name = forms.CharField(label='Полное:', widget=forms.TextInput(attrs={'placeholder': 'Наименование'}),
                                required=True, max_length=255)
    email = forms.EmailField(label='Почта:', widget=forms.TextInput(attrs={'placeholder': 'name@domain.ru'}),
                             required=False)
    phone = forms.CharField(label='Телефон:', required=False,
                            widget=forms.TextInput(attrs={'placeholder': '+79999999999'}))
    phone2 = forms.CharField(label='Телефон доп:', widget=forms.TextInput(attrs={'placeholder': '+79999999999'}),
                             required=False)
    address = forms.CharField(label='Адрес:', required=False,
                              widget=forms.Textarea(attrs={'rows': '3','placeholder': 'Город, Улица, Дома, офис.'}))
    post_address = forms.CharField(label='Почтовый адрес:', required=False,
                                   widget=forms.Textarea(
                                       attrs={'rows': '3', 'placeholder': 'Город, Улица, Дома, офис.'}))
    INN = forms.CharField(label='ИНН:', widget=forms.TextInput(attrs={'placeholder': '123456789'}),
                          required=True, max_length=12)
    KPP = forms.CharField(label='КПП:', widget=forms.TextInput(attrs={'placeholder': '123456789'}),
                          required=False, max_length=9)
    director = forms.CharField(label='Руководитель:',
                               widget=forms.TextInput(attrs={'placeholder': 'Иванов Иван Иванович'}),
                               required=False, max_length=128)
    description = forms.CharField(label='Примечание:', required=False,
                                  widget=forms.Textarea(attrs={'rows': '3', 'placeholder': 'Примечание'}))

