from django.urls import path
from . import views as products_views

urlpatterns = [
     path('', products_views.ProductList.as_view(), name='products_list'),
     path('categories', products_views.CategoriesList.as_view(), name='categories'),
     path('categories/new', products_views.CatCreateView.as_view(), name='products_cat_new'),
     path('categories/<str:slug>/edit', products_views.CatUpdateView.as_view(), name='products_cat_edit'),
     path('categories/<str:slug>/del', products_views.CatDeleteView.as_view(), name='products_cat_del'),
     path('cat/<str:slug>/', products_views.ProductList.as_view(), name='products_list_by_cat'),
     path('new', products_views.ProductCreateView.as_view(), name='products_new'),

]