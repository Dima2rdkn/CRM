from django.shortcuts import redirect
from documents.invoices.models import Invoice
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InvoiceEditForm, InvoiceFormSet


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = InvoiceEditForm
    template_name = 'documents/invoice/invoice.html'
    context_object_name = 'invoice'
    object = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['invoice_formset'] = InvoiceFormSet(self.request.POST, instance=self.object)
        else:
            context['invoice_formset'] = InvoiceFormSet(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        invoice_formset = InvoiceFormSet(self.request.POST)
        if form.is_valid() and invoice_formset.is_valid():
            return self.form_valid(form, invoice_formset)
        else:
            return self.form_invalid(form, invoice_formset)

    def form_valid(self, form, invoice_formset):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        result = form.save()
        # saving invoice_formset
        invoice_formset.instance = result
        invoice_formset.save()
        return redirect("invoices")

    def form_invalid(self, form, invoice_formset):
        return self.render_to_response(
            self.get_context_data(form=form, image_formset=invoice_formset))


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    form_class = InvoiceEditForm
    template_name = 'documents/invoice/invoice.html'
    context_object_name = 'invoice'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['invoice_formset'] = InvoiceFormSet(self.request.POST)
        else:
            context['invoice_formset'] = InvoiceFormSet(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        invoice_formset = InvoiceFormSet(self.request.POST, instance=self.object)
        if form.is_valid() and invoice_formset.is_valid():
            return self.form_valid(form, invoice_formset)
        else:
            return self.form_invalid(form, invoice_formset)

    def form_valid(self, form, invoice_formset):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        result = form.save()
        # saving invoice_formset
        invoice_formset.instance = result
        invoice_formset.save()
#        return super().form_valid(form)
        return redirect("invoices")

    def form_invalid(self, form, invoice_formset):
        return self.render_to_response(
            self.get_context_data(form=form, invoice_formset=invoice_formset))


class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    context_object_name = 'invoice'
    template_name = 'documents/invoice/invoices.html'
