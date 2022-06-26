import vobject
import base64
from django.shortcuts import render, get_object_or_404
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


def contactsImport(request):
    if request.method == 'POST':
        fd = request.FILES['file']
        """
        Убираем переносы строк, так как vobject 
        нифига не умеет читать перенесенные строки, а
        в vcard строки длиннее 75 символов, переносятся на новую строку 
        с символом '='
        Ну и переводим за одним в кодировку utf-8
        """
        fd = fd.read().decode('utf-8').replace("=\r\n=", '=').replace("=\r\n;", '=;')
        # Считываем все vcard из файла
        vcardlist = vobject.readComponents(fd)
        # Готовим словарь
        flist = {}
        for vcard in vcardlist:
            # Проверяем реквизиты объекта на наличие соответствуюших атрибутов
            # и загоняем все имеющиеся в список.
            if hasattr(vcard, 'fn'):
                while vcard.contents['fn'][0].value in flist:
                    vcard.contents['fn'][0].value = vcard.contents['fn'][0].value+"*"
                if hasattr(vcard, 'tel'):
                    cell = [tel.value for tel in vcard.contents['tel']]
                else:
                    cell = []
                if hasattr(vcard, 'photo'):
                    # фото в шаблон нужно передавать в utf-8 Base64 кодировке, а
                    # vobject уже постарался считать в каком-то бинарном формате
                    # по-этому переводим все обратно.
                    strphoto = base64.b64encode(vcard.photo.value).decode('utf-8')
                else:
                    strphoto = ""
                if hasattr(vcard, 'email'):
                    email = [email.value for email in vcard.contents['email']]
                else:
                    email = []
                vcardvalue = [cell, email, strphoto]
                flist.update({vcard.contents['fn'][0].value: vcardvalue})
        # сортируем, для красоты
        sortedlist = sorted(flist.keys())
        sorteddict = {}
        for element in sortedlist:
            sorteddict[element] = flist[element]
        # и отправляем в шаблон...
        return render(request, 'references/contacts/import.html', {'flist': sorteddict})
    return render(request, 'references/contacts/import.html')
