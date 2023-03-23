from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.documents, name='documents'),
    path('invoices/', include('documents.invoices.urls')),
]
