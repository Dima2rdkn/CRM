from django.shortcuts import render, redirect, get_object_or_404

from references.contacts.models import ContactGroup, Contact
from .forms import GroupEditForm, ContactCreateForm
from django.views.generic import UpdateView, DeleteView


class GroupUpdateView(UpdateView):
    model = ContactGroup
    template_name = 'references/contacts/groupedit.html'
    form_class = GroupEditForm


class GroupDeleteView(DeleteView):
    model = ContactGroup
    success_url = '/admin/contacts/groups/'
    template_name = 'references/contacts/group_delete.html'


def contacts_list(request, group_id=None):
    if group_id:
        group = get_object_or_404(ContactGroup, pk=group_id)
        groups = ContactGroup.objects.filter(parent=group)
        contacts = Contact.objects.filter(category=group)
    else:
        group = None
        groups = ContactGroup.objects.all()
        contacts = Contact.objects.all()
    return render(request, 'references/contacts/list.html',
                  {'group': group, 'groups': groups, 'contacts': contacts})


def contact_groups(request):
    groups = ContactGroup.objects.all()
    return render(request, 'references/contacts/groups.html', {'groups': groups})


def group_edit(request):
    error = ""
    if request.method == "POST":
        form = GroupEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_groups_edit')
        else:
            error = "Ошибка заполнения формы!"
    form = GroupEditForm()
    params = {
        "form": form,
        "Error": error,
    }
    return render(request, 'references/contacts/groupedit.html', params)
