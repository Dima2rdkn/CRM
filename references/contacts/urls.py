from django.urls import path
from . import views as contacts_views


urlpatterns = [
path('', contacts_views.contacts_list, name='clients'),
path('contacts/<int:group_id>/', contacts_views.contacts_list,
     name='contacts_list_by_group'),
path('contacts/<int:group_id>/edit/', contacts_views.contacts_group_edit,
     name='contacts_group_edit'),
path('contacts/newgroup/', contacts_views.contacts_group_edit,
     name='contacts_group_new'),
path('contacts/element/<int:contact_id>/', contacts_views.contact_detail,
     name='contact_detail'),
path('contacts/element/<int:contact_id>/edit/', contacts_views.contact_edit,
     name='contact_edit'),
path('contacts/element/new/', contacts_views.contact_edit,
     name='contact_new'),
]
