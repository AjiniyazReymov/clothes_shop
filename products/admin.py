from django.contrib import admin
from .models import Product, ProductReview, Category, Order, OrderItem, PageView


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'stock', 'available', 'category']
    list_filter = ['price', 'available']
    search_fields = ['name', 'description']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'paid']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

class PageViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_id', 'url', 'ip_address', 'user_agent']
    list_filter = ['url', 'ip_address']

admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(PageView, PageViewAdmin)