from django.contrib import admin

from .models import *


admin.site.register(Category)
admin.site.register(Hoodies, HoodieAdmin)
admin.site.register(Tshirt)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)