from django.urls import path
from . import views as measure_views

urlpatterns = [
     path('', measure_views.MeasureList.as_view(), name='measure_list'),
     path('new', measure_views.MeasureCreateView.as_view(), name='measure_new'),
     path('<str:slug>/del', measure_views.MeasureDeleteView.as_view(), name='measure_del'),
     path('<str:slug>', measure_views.MeasureUpdateView.as_view(), name='measure_detail')
]
