from django.contrib import admin

from .models import Staff
from .models import Product
from .models import Order
from .models import ProductOrder


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['staff', 'complete', 'time_in', 'time_out']
    search_fields = ['staff__full_name', 'time_in', 'time_out']


admin.site.register(Staff)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(ProductOrder)
