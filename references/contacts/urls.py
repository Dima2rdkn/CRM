from django.urls import path
from . import views as contacts_views


urlpatterns = [
     path('', contacts_views.contacts_list, name='contacts'),
     path('group/<int:group_id>/', contacts_views.contacts_list,
          name='contacts_list_by_group'),
     path('groups/', contacts_views.contact_groups, name='contact_groups_edit'),
     path('groups/new', contacts_views.group_edit, name='contact_groups_new'),
     path('groups/<int:pk>', contacts_views.GroupUpdateView.as_view(), name='contact_group_edit'),
     path('groups/<int:pk>/del', contacts_views.GroupDeleteView.as_view(), name='contact_group_delete'),
]
