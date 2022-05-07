from django.shortcuts import render, get_object_or_404
from references.products.models import Categories, Products, ProductImages, Specifications, Feedback
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CatEditForm, ProductEditForm

class ProductList(ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'references/products/list.html'


class CategoriesList(ListView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'references/products/categories.html'


class CatCreateView(LoginRequiredMixin, CreateView):
    model = Categories
    form_class = CatEditForm
    template_name = 'references/products/catedit.html'


class CatUpdateView(LoginRequiredMixin, UpdateView):
    model = Categories
    form_class = CatEditForm
    template_name = 'references/products/catedit.html'


class CatDeleteView(LoginRequiredMixin, DeleteView):
    model = Categories
    context_object_name = 'categories'
    template_name = 'references/products/cat_delete.html'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductEditForm
    template_name = 'references/products/edit.html'