from django.urls import path
from . import views as suppliers_views

urlpatterns = [
     path('', suppliers_views.suppliers_list, name='suppliers'),
     path('group/<int:group_id>/', suppliers_views.suppliers_list,
          name='suppliers_list_by_group'),
     path('groups/', suppliers_views.suppliers_groups, name='suppliers_groups_edit'),
     path('groups/new', suppliers_views.GroupCreateView.as_view(), name='suppliers_groups_new'),
     path('groups/<int:pk>', suppliers_views.GroupUpdateView.as_view(), name='suppliers_group_edit'),
     path('groups/<int:pk>/del', suppliers_views.GroupDeleteView.as_view(), name='suppliers_group_delete'),
     path('<int:pk>', suppliers_views.SupplierDetailView.as_view(), name='supplier_detail'),
     path('new', suppliers_views.SupplierCreateView.as_view(), name='suppliers_new'),
     path('<int:pk>/edit', suppliers_views.SupplierUpdateView.as_view(), name='supplier_edit'),
     path('<int:pk>/del', suppliers_views.SupplierDeleteView.as_view(), name='supplier_delete'),
]
