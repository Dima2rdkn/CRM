from django.shortcuts import render, redirect, get_object_or_404
from references.contacts.models import ContactGroup, Contact
from .forms import GroupEditForm, ContactEditForm
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = ContactGroup
    template_name = 'references/contacts/groupedit.html'
    form_class = GroupEditForm


class GroupDeleteView(LoginRequiredMixin, DeleteView):
    model = ContactGroup
    success_url = '/admin/contacts/groups/'
    template_name = 'references/contacts/group_delete.html'


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = ContactGroup
    template_name = 'references/contacts/groupedit.html'
    form_class = GroupEditForm


class ContactDetailView(LoginRequiredMixin, DetailView):
    model = Contact
    template_name = 'references/contacts/detail.html'
    context_object_name = 'contact'


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'references/contacts/edit.html'
    form_class = ContactEditForm

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        return super().form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'references/contacts/edit.html'
    form_class = ContactEditForm

    def form_valid(self, form):
        form.instance.createdBy = self.request.user
        form.instance.isActive = True
        return super().form_valid(form)


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'references/contacts/edit.html'


def contacts_list(request, group_id=None):
    if group_id:
        group = get_object_or_404(ContactGroup, pk=group_id)
        groups = ContactGroup.objects.filter(parent=group)
        contacts = Contact.objects.filter(category=group)
    else:
        group = None
        groups = ContactGroup.objects.all()
        contacts = Contact.objects.all()
    return render(request, 'references/contacts/contacts.html',
                  {'group': group, 'groups': groups, 'contacts': contacts})


def contact_groups(request):
    groups = ContactGroup.objects.all()
    return render(request, 'references/contacts/groups.html', {'groups': groups})
