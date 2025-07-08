from django.contrib import admin

from .models import *

admin.site.register(product)
admin.site.register(User_details)
admin.site.register(category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(employee)
admin.site.register(task)
admin.site.register(book)
admin.site.register(publisher)
class AdminOrderItemInline(admin.TabularInline):
    model = admin_order_item
    extra = 0

class AdminOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'total']
    inlines = [AdminOrderItemInline]

admin.site.register(admin_order, AdminOrderAdmin)