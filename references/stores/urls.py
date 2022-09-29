from django.urls import path
from . import views as stores_views

urlpatterns = [
     path('', stores_views.StoresList.as_view(), name='stores_list'),
     path('new', stores_views.StoreCreateView.as_view(), name='stores_new'),
     path('<str:slug>/del', stores_views.StoreDeleteView.as_view(), name='store_del'),
     path('<str:slug>', stores_views.StoreUpdateView.as_view(), name='store_detail')
]
