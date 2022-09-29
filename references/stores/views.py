from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from references.stores.models import Stores
from .forms import StoreEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse


class StoresList(ListView):
    model = Stores
    context_object_name = 'stores'
    template_name = 'references/stores/list.html'


class StoreCreateView(LoginRequiredMixin, CreateView):
    model = Stores
    form_class = StoreEditForm
    template_name = 'references/stores/edit.html'

    def get_success_url(self):
        return reverse('stores_list')


class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = Stores
    form_class = StoreEditForm
    template_name = 'references/stores/edit.html'

    def get_success_url(self):
        return reverse('stores_list')


class StoreDeleteView(LoginRequiredMixin, DeleteView):
    model = Stores
    context_object_name = 'stores'
    template_name = 'references/stores/delete.html'

    def get_success_url(self):
        return reverse('stores_list')
