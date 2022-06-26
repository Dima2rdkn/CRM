from django.urls import path
from . import views as contacts_views

urlpatterns = [
     path('', contacts_views.contacts_list, name='contacts'),
     path('group/<int:group_id>/', contacts_views.contacts_list,
          name='contacts_list_by_group'),
     path('groups/', contacts_views.contact_groups, name='contact_groups_edit'),
     path('groups/new', contacts_views.GroupCreateView.as_view(), name='contact_groups_new'),
     path('groups/<int:pk>', contacts_views.GroupUpdateView.as_view(), name='contact_group_edit'),
     path('groups/<int:pk>/del', contacts_views.GroupDeleteView.as_view(), name='contact_group_delete'),
     path('<int:pk>', contacts_views.ContactDetailView.as_view(), name='contact_detail'),
     path('new', contacts_views.ContactCreateView.as_view(), name='contacts_new'),
     path('<int:pk>/edit', contacts_views.ContactUpdateView.as_view(), name='contacts_edit'),
     path('<int:pk>/del', contacts_views.ContactDeleteView.as_view(), name='contacts_delete'),
     path('import/', contacts_views.contactsImport, name='contacts_import'),
]
