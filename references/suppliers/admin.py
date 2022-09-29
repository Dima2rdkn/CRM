from django.contrib import admin
from references.suppliers.models import Supplier, SupplierGroup


admin.site.register(Supplier)
admin.site.register(SupplierGroup)
