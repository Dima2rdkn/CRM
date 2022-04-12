from django.contrib import admin
from references.contacts.models import Contact, ContactGroup


admin.site.register(Contact)
admin.site.register(ContactGroup)
