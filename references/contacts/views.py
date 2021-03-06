import vobject
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from references.contacts.models import ContactGroup, Contact, ContactTmp
from .forms import GroupEditForm, ContactEditForm
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


class ContactDeleteView(LoginRequiredMixin, DeleteView):
    model = Contact
    template_name = 'references/contacts/edit.html'

@login_required
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

@login_required
def contacts_import(request):
    contacts = ContactTmp.objects.all()
    if contacts.count() > 0:
        if request.method == 'POST' and request.POST.get("clear"):
            items = request.POST.getlist("item")
            for item in items:
                ContactTmp.objects.filter(id=item).delete()
            return render(request, 'references/contacts/import.html', {'flist': contacts_paginator(request)})
        if request.method == 'POST' and request.POST.get("import"):
            items = request.POST.getlist("item")
            for item in items:
                contact_tmp = ContactTmp.objects.get(id=item)
                if contact_tmp.image:
                    str64 = contact_tmp.image
                    ext = ".jpg"
                    data = ContentFile(base64.b64decode(str64), name='contact_'+str(item) + ext)
                else:
                    data = None
                contact = Contact(first_name=contact_tmp.first_name,
                                  last_name=contact_tmp.last_name,
                                  email=contact_tmp.email,
                                  phone=contact_tmp.phone,
                                  phone2=contact_tmp.phone2,
                                  address=contact_tmp.address,
                                  description=contact_tmp.description,
                                  createdBy=request.user,
                                  image=data)
                contact.save()
                ContactTmp.objects.filter(id=item).delete()
            return render(request, 'references/contacts/import.html',
                          {"message": "??????????????????????????: "+str(len(items))+" ??????????????!"})
        return render(request, 'references/contacts/import.html', {'flist': contacts_paginator(request)})
    else:
        print("--------------------------> Load")
        if request.method == 'POST' and request.POST.get("load_file"):
            fd = request.FILES['file']
            if fd:
                """
                ?????????????? ???????????????? ??????????, ?????? ?????? vobject 
                ???????????? ???? ?????????? ???????????? ???????????????????????? ????????????, ??
                ?? vcard ???????????? ?????????????? 75 ????????????????, ?????????????????????? ???? ?????????? ???????????? 
                ?? ???????????????? '='
                ???? ?? ?????????????????? ???? ?????????? ?? ?????????????????? utf-8
                """
                fd = fd.read().decode('utf-8').replace("=\r\n=", '=').replace("=\r\n;", ';')
                # ?????????????????? ?????? vcard ???? ??????????
                vcardlist = vobject.readComponents(fd)
                for vcard in vcardlist:
                    # ?????????????????? ?????????????????? ?????????????? ???? ?????????????? ?????????????????????????????? ??????????????????
                    # ?? ???????????????? ?????? ?????????????????? ?? ????????????.
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
                            # ???????? ?? ???????????? ?????????? ???????????????????? ?? utf-8 Base64 ??????????????????, ??
                            # vobject ?????? ???????????????????? ?????????????? ?? ??????????-???? ???????????????? ??????????????
                            # ????-?????????? ?????????????????? ?????? ??????????????.
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
                        # ?? ???????????????????? ?? ????????????...
                return render(request, 'references/contacts/import.html', {'flist': contacts_paginator(request)})
            else:
                return render(request, 'references/contacts/import.html',
                              {"message": "???????? ???? ????????????, ?????? ???? ???????????????? ??????????????!"})
    return render(request, 'references/contacts/import.html')

