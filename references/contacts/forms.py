from django import forms
from .models import ContactGroup, Contact

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        fields = ['parent', 'title', 'description']

    parent = forms.ModelChoiceField(label='Группа:', queryset=ContactGroup.objects.all())
    title = forms.CharField(label='Наименование:', widget=forms.TextInput(attrs={'placeholder': 'Наименование'}))
    description = forms.CharField(label='Примечание:',
                                  widget=forms.TextInput(attrs={'placeholder': 'Краткое описание'}))


class ContactCreateForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    image = forms.ImageField(label='Фото:')
    category = forms.ModelChoiceField(label='Группа:', queryset=ContactGroup.objects.all())
    first_name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
                                 required=True, max_length=100)
    last_name = forms.CharField(label='Фамилия:', widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                                required=False, max_length=200)
    email = forms.EmailField(label='Почта:', widget=forms.TextInput(attrs={'placeholder': 'name@domain.ru'}),
                             required=False)
    phone = forms.CharField(label='Телефон:', widget=forms.TextInput(attrs={'placeholder': '+79999999999'}))
    phone2 = forms.CharField(label='Телефон:', widget=forms.TextInput(attrs={'placeholder': '+79999999999'}),
                             required=False)
    messenger = forms.ChoiceField(label='Мессенджер:', choices=Contact.MESSENGERS)
    address = forms.CharField(label='Адрес', widget=forms.TextInput(attrs={'placeholder': 'Город, Улица, Дома, Кв.'}))
    description = forms.CharField(label='Примечание:', widget=forms.TextInput(attrs={'placeholder': 'Примечание'}))
