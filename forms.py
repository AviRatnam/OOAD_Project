from django import forms

from .models import Stocksymbol, Stockprice, Transactions

class StocksymbolForm(forms.ModelForm):
    """docstring for StocksymbolForm"""
    class Meta:
        model = Stocksymbol
        fields = ('s_id','symbol', 'title','price',)

class StockpriceForm(forms.ModelForm):
    """docstring for StockpriceForm"""
    class meta:
        model = Stockprice
        fields = ('stock_id','date','open_price','high','low','close_price','adjusted_close','volume')

class TransactionsForm(forms.ModelForm):
    class Meta:
        model = Transactions
        fields = ('stock_id','transaction_date','user','type_transaction','price_per_stock','numstocks')