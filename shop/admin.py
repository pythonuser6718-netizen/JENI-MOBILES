from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ContactMessage, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'discount_price', 'stock', 'photo_preview', 'is_featured', 'is_new')
    list_filter = ('category', 'brand', 'is_featured', 'is_new')
    search_fields = ('name', 'brand')
    prepopulated_fields = {'slug': ('brand', 'name')}
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:50px;border-radius:6px;" />', obj.photo.url)
        return '—'
    photo_preview.short_description = 'Preview'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'total', 'status', 'created_at')
    list_filter = ('status',)
    inlines = [OrderItemInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
