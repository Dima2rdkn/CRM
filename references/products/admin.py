from django.contrib import admin
from references.products.models import Categories, Products, ProductImages, Specifications, Feedback

admin.site.register(ProductImages)
admin.site.register(Specifications)
admin.site.register(Feedback)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

