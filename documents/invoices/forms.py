from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceTable
from references.products.models import Products
from references.suppliers.models import Supplier
from references.stores.models import Stores
from references.measure.models import Measure
from datetime import datetime


class InvoiceEditForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ('createdBy', 'createdOn', 'isActive')

    docNum = forms.CharField(label='Номер:', widget=forms.TextInput(attrs={'size': 20}), required=True, max_length=16,)
    docDate = forms.DateTimeField(required=True, label='Дата:', input_formats=['%Y-%m-%dT%H:%M'],
                                  widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M',
                                                             attrs={'type': 'datetime-local'}),
                                  initial=datetime.now(),
                                  localize=True)
    supplier = forms.ModelChoiceField(label='Поставщик:', queryset=Supplier.get_list())
    store = forms.ModelChoiceField(label='Склад:', queryset=Stores.get_list())


class InvoiceTabEditForm(forms.ModelForm):
    class Meta:
        model = InvoiceTable
        exclude = ('docptr',)

    product = forms.ModelChoiceField(label='Товар:', queryset=Products.get_list(),
                                     widget=forms.Select(attrs={'style': 'width: 240px'}))
    quantity = forms.FloatField(label='Количество:', widget=forms.TextInput(attrs={'size': 10}),
                                min_value=0.01, required=True)
    mt = forms.ModelChoiceField(label='Единица измерения:', queryset=Measure.objects.all())
    price = forms.FloatField(label='Цена:', widget=forms.TextInput(attrs={'size': 10}), required=False)


InvoiceFormSet = inlineformset_factory(
    Invoice,
    InvoiceTable,
    form=InvoiceTabEditForm,
    extra=1,
    can_delete=True,
    can_order=True,
    # fk_name=None,
    # fields=('image', 'primary'),
    # fields=None, exclude=None, can_order=False,
    # max_num=None, formfield_callback=None,
    # widgets=None, validate_max=False, localized_fields=None,
    # labels=None, help_texts=None, error_messages=None,
    # min_num=None, validate_min=False, field_classes=None
)
