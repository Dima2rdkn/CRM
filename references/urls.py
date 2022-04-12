from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.references, name='references'),
    path('contacts/', include('references.contacts.urls')),
]
