from django.contrib import admin
from .models import Cart, Users, Categories, Subcategories, Store, Orders, Providers, OrderDetails, Measure_units   # Importa i tuoi modelli

admin.site.register(Cart)
admin.site.register(Users)
admin.site.register(Categories)
admin.site.register(Subcategories)
admin.site.register(Store)
admin.site.register(Orders)
admin.site.register(OrderDetails)
admin.site.register(Providers)
admin.site.register(Measure_units)
