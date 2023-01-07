from django import forms
from .models import ContactGroup, Contact

class GroupEditForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        fields = ['parent', 'title', 'description']


class ContactEditForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('createdBy', 'createdOn', 'isActive')

    category = forms.ModelChoiceField(label='Группа:', queryset=ContactGroup.objects.all())
    image = forms.ImageField(label='Фото:', required=False,
                             widget=forms.ClearableFileInput(attrs={'id': 'avatar'}))
    first_name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
                                 required=True, max_length=100)
    last_name = forms.CharField(label='Фамилия:', widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                                required=False, max_length=200)
    email = forms.EmailField(label='Почта:', widget=forms.TextInput(attrs={'placeholder': 'name@domain.ru'}),
                             required=False)
    phone = forms.CharField(label='Телефон:', widget=forms.TextInput(attrs={'placeholder': '+79999999999'}))
    phone2 = forms.CharField(label='Телефон доп:', widget=forms.TextInput(attrs={'placeholder': '+79999999999'}),
                             required=False)
    messenger = forms.ChoiceField(label='Мессенджер:', choices=Contact.MESSENGERS)
    address = forms.CharField(label='Адрес',
                              widget=forms.Textarea(attrs={'rows': '3', 'placeholder': 'Город, Улица, Дома, Кв.'}))
    description = forms.CharField(label='Примечание:', required=False,
                                    widget=forms.Textarea(attrs={'rows': '3', 'placeholder': 'Примечание'}))

