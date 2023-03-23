from django.shortcuts import redirect
from django.urls import reverse
from references.products.models import Categories, Products, ProductImages, \
    Specifications, Feedback
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CatEditForm, ProductEditForm, ImageFormSet


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
    template_name = 'references/products/delete.html'


class ProductList(LoginRequiredMixin, ListView):
    model = Products
    context_object_name = 'products'
    # В list.html нужно передать товары, категории или Выбранная категория
    template_name = 'references/products/list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        if ('slug' in self.kwargs) and (self.kwargs['slug']):
            selected = Categories.get_list(slug=self.kwargs['slug'])
            context['products'] = Products.get_list_image(category=selected)
            context['group'] = selected
        else:
            context['group'] = ""
            context['products'] = Products.get_list_image()
        category = Categories.get_list()
        context['category'] = category

        # context['products_search'] = searched_products(self.request.GET.get('q'), category)
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Products
    template_name = 'references/products/detail.html'
    context_object_name = 'product'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        images = ProductImages.objects.all().filter(product=self.object)
        context['product_images'] = images
        context['primary_image'] = images.filter(primary=True).first()
        # context['products_search'] = searched_products(self.request.GET.get('q'), category)
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = ProductEditForm
    template_name = 'references/products/edit.html'
    object = None
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, instance=self.object)
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_formset = ImageFormSet(self.request.POST, self.request.FILES)
        if form.is_valid() and image_formset.is_valid():
            return self.form_valid(form, image_formset)
        else:
            return self.form_invalid(form, image_formset)

    def form_valid(self, form, image_formset):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        self.object = form.save()
        # saving image_formset
        image_formset.instance = self.object
        image_formset.save()
        # images_meta = image_formset.save(commit=False)
        # for meta in images_meta:
        #     meta.product = self.object
        #     meta.save()
        return redirect("products_list")

    def form_invalid(self, form, image_formset):
        return self.render_to_response(
            self.get_context_data(form=form, image_formset=image_formset))


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Products
    form_class = ProductEditForm
    template_name = 'references/products/edit.html'
    object = None
    context_object_name = 'product'

    def get_success_url(self):
        self.success_url = reverse("product_detail", slug=self.object.slug)
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = ImageFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        image_formset = ImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        if form.is_valid() and image_formset.is_valid():
            return self.form_valid(form, image_formset)
        else:
            return self.form_invalid(form, image_formset)

    def form_valid(self, form, image_formset):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        self.object = form.save()
        # saving image_formset
        image_formset.instance = self.object
        image_formset.save()
        return redirect("product_detail", slug=self.object.slug)

    def form_invalid(self, form, image_formset):
        return self.render_to_response(
            self.get_context_data(form=form, image_formset=image_formset))
