from django.shortcuts import render, get_object_or_404
from .models import SupplierGroup, Supplier
from .forms import GroupEditForm, SupplierEditForm
from django.db.models import Q
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse



class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = SupplierGroup
    template_name = 'references/suppliers/groupedit.html'
    form_class = GroupEditForm


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = SupplierGroup
    success_url = '/admin/suppliers/groups/'
    template_name = 'references/suppliers/group_delete.html'


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = SupplierGroup
    template_name = 'references/suppliers/groupedit.html'
    form_class = GroupEditForm


class SupplierDetailView(LoginRequiredMixin, DetailView):
    model = Supplier
    template_name = 'references/suppliers/detail.html'
    context_object_name = 'supplier'


class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    template_name = 'references/suppliers/edit.html'
    form_class = SupplierEditForm

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        return super().form_valid(form)


class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    template_name = 'references/suppliers/edit.html'
    form_class = SupplierEditForm

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        return super().form_valid(form)


class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'references/suppliers/delete.html'

    def get_success_url(self):
        return reverse('suppliers')


@login_required
def suppliers_list(request, group_id=None):
    sfilter = request.GET.get('Filter')     # Проверяем параметр "Filter" из GET параметра
    if sfilter is None:
        sfilter = ""
    if group_id:
        group = get_object_or_404(SupplierGroup, pk=group_id)
        groups = SupplierGroup.objects.filter(parent=group)
        suppliers = Supplier.objects.filter(
            Q(full_name__icontains=sfilter) |
            Q(name__icontains=sfilter) |
            Q(phone__icontains=sfilter) |
            Q(phone2__icontains=sfilter) |
            Q(INN__icontains=sfilter) |
            Q(category=groups)
                                          )
    else:
        group = None
        groups = SupplierGroup.objects.all()
        suppliers = Supplier.objects.filter(
            Q(full_name__icontains=sfilter) |
            Q(name__icontains=sfilter) |
            Q(phone__icontains=sfilter) |
            Q(phone2__icontains=sfilter) |
            Q(INN__icontains=sfilter) |
            Q(address__icontains=sfilter)
        )
    return render(request, 'references/suppliers/suppliers.html',
                  {'group': group, 'groups': groups, 'suppliers': suppliers})


@login_required
def suppliers_groups(request):
    groups = SupplierGroup.objects.all()
    return render(request, 'references/suppliers/groups.html', {'groups': groups})


@login_required
def suppliers_paginator(request):
    suppliers = Supplier.objects.all()
    paginator = Paginator(suppliers, 25)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return page_obj

