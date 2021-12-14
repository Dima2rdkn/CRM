from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404

from references.contacts.models import ContactGroup, Contact
from .forms import GroupCreateForm, ContactCreateForm


def contacts_list(request, group_id=None):
    group = None
    groups = ContactGroup.objects.all()
    contacts = Contact.objects.all()
    if group_id:
        group = get_object_or_404(ContactGroup, pk=group_id)
        groups = groups.filter(parent=group)
        contacts = contacts.filter(category=group)
    return render(request, 'references/contacts/list.html',
                  {'group': group, 'groups': groups, 'contacts': contacts})


def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'references/contacts/detail.html',
                  {'contact': contact})


def contacts_group_edit(request, group_id=None):
    if group_id is not None:
        group = get_object_or_404(ContactGroup, pk=group_id)
    else:
        group = ContactGroup()
    error = 0
    if request.method == 'POST':
        form = GroupCreateForm(request.POST, instance=group)
        if "Edit" in request.POST:
            if form.is_valid():
                cd = form.cleaned_data
                group.title = cd['title']
                group.parent = cd['parent']
                group.description = cd['description']
                group.save()
        elif "Delete" in request.POST:
            try:
                group.delete()  # удаление категории
            except ProtectedError:
                # тут нужно нормально переписать обработку ошибок
                error = 1
                return render(request, 'references/contacts/group.html',
                              {'group': group, 'form': form, 'error': error})
            # Группа удалена, выводим корень и список
            return render(request, 'references/contacts/list.html')
        # Если ничего на менялось выводим список как и было :-)
        return render(request, 'references/contacts/list.html',
                      {'group': group})
    else:
        form = GroupCreateForm(instance=group)
    return render(request, 'references/contacts/group.html',
                  {'group': group, 'form': form, 'error': error})


def contact_edit(request, contact_id=None):
    if contact_id is not None:
        contact = get_object_or_404(Contact, pk=contact_id)
    else:
        contact = Contact()
    error = 0
    if request.method == 'POST':
        form = ContactCreateForm(request.POST, request.FILES, instance=contact)
        if "Edit" in request.POST:
            if form.is_valid():
                form.save()
        elif "Delete" in request.POST:
            try:
                contact.delete()  # удаление категории
            except ProtectedError:
                # тут нужно нормально переписать обработку ошибок
                error = 1
                return render(request, 'references/contacts/edit.html',
                              {'client': contact,
                               'form': form,
                               'error': error})
        return render(request, 'references/contacts/list.html',
                      {'group': contact.category})
    else:
        form = ContactCreateForm(instance=contact)
    return render(request, 'references/contacts/edit.html',
                  {'client': contact, 'form': form, 'error': error})
