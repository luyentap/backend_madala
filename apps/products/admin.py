from apps.products.models import Category, Product
from django.contrib import admin

# Register your models here.
admin.register(Category)(admin.ModelAdmin)
admin.register(Product)(admin.ModelAdmin)
