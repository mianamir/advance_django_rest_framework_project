from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'amount_available', 'cost', 'seller_id']