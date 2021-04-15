from django import forms

from .models import Stocksymbol, Stockprice, Transactions

class StocksymbolForm(forms.ModelForm):
    """docstring for StocksymbolForm"""
    class Meta:
        model = Stocksymbol
        fields = ('s_id','symbol', 'title',)

class StockpriceForm(forms.ModelForm):
    """docstring for StockpriceForm"""
    class meta:
        model = Stockprice
        fields = ('stock_id','date','open_price','high','low','close_price','adjusted_close','volume')

class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('stock_id','transaction_date','seller','buyer','price_per_stock','numstocks')