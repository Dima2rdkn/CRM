import vobject
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from references.contacts.models import ContactGroup, Contact, ContactTmp
from .forms import GroupEditForm, ContactEditForm
from django.db.models import Q
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

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

# НАДО ПЕРЕДЕЛАТЬ НА УСТАНОВКУ ФЛАГА ISACTIVE в FALSE
class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'references/contacts/edit.html'

@login_required
def contacts_list(request, group_id=None):
    sfilter = request.GET.get('Filter')     # Проверяем параметр "Filter" из GET параметра
    if sfilter is None:
        sfilter = ""
    if group_id:
        group = get_object_or_404(ContactGroup, pk=group_id)
        groups = ContactGroup.objects.filter(parent=group)
        contacts = Contact.objects.filter(
            Q(first_name__icontains=sfilter) |
            Q(last_name__icontains=sfilter) |
            Q(phone__icontains=sfilter) |
            Q(phone2__icontains=sfilter) |
            Q(address__icontains=sfilter) |
            Q(category=groups)
                                          )
    else:
        group = None
        groups = ContactGroup.objects.all()
        contacts = Contact.objects.filter(
            Q(first_name__icontains=sfilter) |
            Q(last_name__icontains=sfilter) |
            Q(phone__icontains=sfilter) |
            Q(phone2__icontains=sfilter) |
            Q(address__icontains=sfilter)
        )
    return render(request, 'references/contacts/contacts.html',
                  {'group': group, 'groups': groups, 'contacts': contacts})


@login_required
def contact_groups(request):
    groups = ContactGroup.objects.all()
    return render(request, 'references/contacts/groups.html', {'groups': groups})


@login_required
def contacts_paginator(request):
    contacts = ContactTmp.objects.all()
    paginator = Paginator(contacts, 25)
    page_number = request.GET.get('page')
    if page_number is None:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return page_obj


"""
Функция импортирует контакты из файла vCard во временную таблицу,
из которой можно переносить записи в таблицу "Клиенты"
"""
@login_required
def contacts_import(request):
    contacts = ContactTmp.objects.all()
    if contacts.count() > 0:    # проверка на существование контактов во временном файле.
        if request.method == 'POST' and request.POST.get("clear"):      # удаляем отмеченные записи
            items = request.POST.getlist("item")
            for item in items:
                ContactTmp.objects.filter(id=item).delete()
            return render(request, 'references/contacts/import.html', {'flist': contacts_paginator(request)})
        if request.method == 'POST' and request.POST.get("import"):     # переносим отмеченные записи в "Клиенты"
            items = request.POST.getlist("item")
            for item in items:
                # обработка перевода картинки из BASE64 в JPG файл.
                contact_tmp = ContactTmp.objects.get(id=item)
                """
                Проверка. Если уже существует запись, или обновляем или пропускаем
                if (Contact.objects.filter(phone=contact_tmp.phone).exists()) \
                        or (Contact.objects.filter(phone=contact_tmp.phone2).exists()) \
                        or (Contact.objects.filter(phone2=contact_tmp.phone).exists()) \
                        or (Contact.objects.filter(phone2=contact_tmp.phone2).exists()):
                    continue
                """
                if contact_tmp.image:
                    str64 = contact_tmp.image
                    ext = ".jpg"
                    data = ContentFile(base64.b64decode(str64), name='contact_'+str(item) + ext)
                else:
                    data = None
                client = Contact(first_name=contact_tmp.first_name,
                                  last_name=contact_tmp.last_name,
                                  email=contact_tmp.email,
                                  phone=contact_tmp.phone,
                                  phone2=contact_tmp.phone2,
                                  address=contact_tmp.address,
                                  description=contact_tmp.description,
                                  createdBy=request.user,
                                  image=data)
                client.save()
                ContactTmp.objects.filter(id=item).delete()
            return render(request, 'references/contacts/import.html',
                          {"message": "Импортировано: "+str(len(items))+" записей!"})
        return render(request, 'references/contacts/import.html', {'flist': contacts_paginator(request)})
    else:   # Временная таблица пустая
        if request.method == 'POST' and request.POST.get("load_file"):  # загружаем данные из vCard
            fd = request.FILES['file']
            if fd:
                """
                Убираем переносы строк, так как vobject 
                нифига не умеет читать перенесенные строки, а
                в vcard строки длиннее 75 символов, переносятся на новую строку 
                с символом '='
                Ну и переводим за одним в кодировку utf-8
                """
                fd = fd.read().decode('utf-8').replace("=\r\n=", '=').replace("=\r\n;", ';')
                # Считываем все vcard из файла
                vcardlist = vobject.readComponents(fd)
                for vcard in vcardlist:
                    # Проверяем реквизиты объекта на наличие соответствуюших атрибутов
                    # и загоняем все имеющиеся в список.
                    if hasattr(vcard, 'fn'):
                        if hasattr(vcard, 'n'):
                            nname = "".join([vcard.n.value.prefix, vcard.n.value.given,
                                              vcard.n.value.suffix, vcard.n.value.additional])
                            fname = vcard.n.value.family
                        else:
                            nname = ""
                            fname = ""
                        if hasattr(vcard, 'tel'):
                            cell = [tel.value for tel in vcard.contents['tel']]
                            cel1=cell[0]
                            if len(cell)>1:
                                cel2=cell[1]
                            else:
                                cel2=""
                        else:
                            cell = ""
                            cel2 = ""
                        if hasattr(vcard, 'address'):
                            address = vcard.address.value
                        else:
                            address = ""
                        if hasattr(vcard, 'org'):
                            org = vcard.org.value
                        else:
                            org = ""
                        if hasattr(vcard, 'photo'):
                            # фото в шаблон нужно передавать в utf-8 Base64 кодировке, а
                            # vobject уже постарался считать в каком-то бинарном формате
                            # по-этому переводим все обратно.
                            strphoto = base64.b64encode(vcard.photo.value).decode('utf-8')
                        else:
                            strphoto = ""
                        if hasattr(vcard, 'email'):
                            email = vcard.email.value
                        else:
                            email = ""
                        contact = ContactTmp(first_name=nname, last_name=fname, email=email, phone=cel1,
                                             phone2=cel2, address=address, description=org, image=strphoto)
                        contact.save()
                        # и отправляем в шаблон...
                return render(request, 'references/contacts/import.html', {'flist': contacts_paginator(request)})
            else:
                return render(request, 'references/contacts/import.html',
                              {"message": "Файл не выбран, или не содержит записей!"})
    return render(request, 'references/contacts/import.html')

