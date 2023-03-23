from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('admin/', views.admin, name='admin'),
    path('references/', include('references.urls')),
    path('documents/', include('documents.urls')),
]
