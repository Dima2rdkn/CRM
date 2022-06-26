from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from references.products.models import Categories, Products, ProductImages, Specifications, Feedback
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CatEditForm, ProductEditForm, ImageFormSet

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

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['image_formset'] = ImageFormSet()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_formset = ImageFormSet(self.request.POST)
        if form.is_valid() and image_formset.is_valid():
            return self.form_valid(form, image_formset)
        else:
            return self.form_invalid(form, image_formset)

    def form_valid(self, form, image_formset):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        self.object = form.save(commit=False)
        self.object.save()
        # saving image_formset
        images_meta = image_formset.save(commit=False)
        for meta in images_meta:
            meta.product = self.object
            meta.save()
        return redirect(reverse("products_list"))

    def form_invalid(self, form, image_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  image_formset=image_formset
                                  )
        )
