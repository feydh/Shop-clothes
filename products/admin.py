from django.contrib import admin
from products.models import Product
from django.contrib.admin import ModelAdmin

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('image', 'name','description', 'price', 'quantity', 'categorys')
    search_fields = ('name', 'price', 'quantity', 'categorys')
    list_filter = ('price', 'quantity')
    fieldsets = (
        ('Product info', {'fields': ('name', 'description', 'price', 'image')}),
    )