from django.contrib import admin
from .models import User,Goods,Address,Order,Orders
 
# Register your models here.
admin.site.register(User)
admin.site.register(Goods)
admin.site.register(Address)
admin.site.register(Orders)
admin.site.register(Order)