from django.db import models

# Create your models here.
from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone

class Stocksymbol(models.Model):
    s_id = models.IntegerField(unique=True)
    symbol = models.CharField(max_length=7,unique=True)
    title = models.CharField(max_length=500)

    def __str__(self):
        return self.symbol

class Stockprice(models.Model):
    pid = models.AutoField(primary_key = True)
    stock_id = models.ForeignKey(Stocksymbol, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.DecimalField(decimal_places=2, max_digits=6)
    high = models.DecimalField(decimal_places=2, max_digits=6)
    low = models.DecimalField(decimal_places=2, max_digits=6)
    close_price = models.DecimalField(decimal_places=2, max_digits=6)
    adjusted_close = models.DecimalField(decimal_places=2, max_digits=6)
    volume = models.IntegerField()

    def __str__(self):
        return self.pid

class Transactions(models.Model):
    tid = models.AutoField(primary_key=True)
    stock_id = models.ForeignKey(Stocksymbol, on_delete=models.CASCADE)
    transaction_date = models.DateField(default=datetime.today)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "seller")
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name = "buyer")
    price_per_stock = models.DecimalField(decimal_places=2, max_digits=6) 
    numstocks = models.IntegerField()

    def __str__(self):
        return self.tid

