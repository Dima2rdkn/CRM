from django.urls import path
from . import views as docs_views

urlpatterns = [
     path('', docs_views.InvoiceListView.as_view(), name='invoices'),
     path('new', docs_views.InvoiceCreateView.as_view(), name='invoice_new'),
     path('<int:pk>/edit', docs_views.InvoiceUpdateView.as_view(), name='invoice_edit'),
]
