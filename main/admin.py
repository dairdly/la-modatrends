from django.contrib.auth.models import Group, User
from django.contrib import admin

from main.models import Product,  Order, Message

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'productType', 'price')
    list_filter = ('category', 'productType', 'rating', 'label')
    fieldsets = (
        ('Details', {
            'classes': ('wide',),
            'fields': ('name', 'category', 'productType', 'price', 'image', 'rating', 'label', 'labelColor', 'description',),
        }),
    )
    search_fields = ('name', 'category', 'productType')
    ordering = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'totalCost', 'status',)
    list_filter = ('city', 'status',)
    readonly_fields = ('date_ordered', 'products',)
    fieldsets = (
        ('User Info', {
            'classes': ('wide',),
            'fields': ('user', 'address', 'apartment', 'city','state',),
        }),
        ('Contact Info', {
            'classes': ('wide',),
            'fields': ('phone', 'email',),
        }),
        ('Order details', {
            'classes': ('wide',),
            'fields': ('status','date_ordered', 'products', 'totalCost', 'notes',),
        }),
    )
    search_fields = ('user', 'city', 'status',)
    ordering = ('-date_ordered',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status',)
    list_filter = ('status',)
    readonly_fields = ('date_sent',)
    fieldsets = (
        ('Details', {
            'classes': ('wide',),
            'fields': ('name', 'phone', 'email', 'status', 'date_sent', 'content',),
        }),
    )
    search_fields = ('name', 'content',)
    ordering = ('-date_sent',)

admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.site_header = 'La-moda Trends'