##################################################################################
#
#   Модели для работы с ТОВАРАМИ И УСЛУГАМИ
#   (С)2022 Дворядкин Дмитрий aka dima2rdkn
###################################################################################

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from references.suppliers.models import Supplier
from references.measure.models import Measure
from references.stores.models import Stores
from references.products.models import Products

########################################
# Накладная
# по документу "Накладная" приходуется товар
#
# Логика включает две модели базовую (Invoice) и табличную (InvoiceTable)


class Invoice(models.Model):
    docNum = models.CharField(max_length=16, verbose_name='Номер')
    docDate = models.DateTimeField(verbose_name='Дата')
    supplier = models.ForeignKey(Supplier, verbose_name='Поставщик', on_delete=models.PROTECT)
    store = models.ForeignKey(Stores, verbose_name='Склад', on_delete=models.PROTECT)
    createdBy = models.ForeignKey(User, related_name='invoice_author', on_delete=models.PROTECT,
                                  verbose_name='Автор')
    createdOn = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    isActive = models.BooleanField(default=True)

    @property
    def summa(self):
        invoice_table = InvoiceTable.objects.filter(docptr=self)
        summa_doc = 0
        for row in invoice_table:
            summa_doc += row.quantity * row.price
        return summa_doc

    def __str__(self):
        return "Накладная"+self.docNum+" от "+self.docDate

    def get_absolute_url(self):
        return reverse('invoice_edit', args=[self.id])

    class Meta:
        verbose_name = 'Накладная'
        verbose_name_plural = 'Накладные'


class InvoiceTable(models.Model):
    docptr = models.ForeignKey(Invoice, verbose_name='Накладная', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.FloatField(verbose_name='Количество')
    mt = models.ForeignKey(Measure, verbose_name='ед. изм.', on_delete=models.PROTECT)
    price = models.FloatField(verbose_name='Цена')

    def __str__(self):
        return self.docptr + "( " + self.product + ")"

    class Meta:
        verbose_name = 'Накладная ТЧ'
        verbose_name_plural = 'Накладная ТЧ'
