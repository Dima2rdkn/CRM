from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.references, name='references'),
    path('contacts/', include('references.contacts.urls')),
    path('products/', include('references.products.urls')),
    path('suppliers/', include('references.suppliers.urls')),
    path('stores/', include('references.stores.urls')),
    path('measure/', include('references.measure.urls')),
]
