from django.contrib import admin
from goods.models import User,Goods,Address,Order,Orders

# Register your models here.
admin.site.register(User)
admin.site.register(Goods)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Orders)