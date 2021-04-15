from django.contrib import admin
from .models import Stocksymbol, Stockprice, Transactions
# Register your models here.
admin.site.register(Stocksymbol)
admin.site.register(Stockprice)
admin.site.register(Transactions)


