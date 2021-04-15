from django.shortcuts import render, redirect
from .forms import StocksymbolForm, StockpriceForm, TransactionsForm
from .models import Transactions
from django.db.models import Q

# Create your views here.
def home_page(request):
    return render(request,'main/home_page.html',{})

def new_stocksymbol(request):
    if request.method == "POST":
        form = StocksymbolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = StocksymbolForm()
    return render(request, 'main/new_stocksymbol.html', {'form': form})

def live_stocks(request):
    return render(request,'main/live_stocks.html',{})

def user_profile(request):
    return render(request,'main/user_profile.html',{})

def transaction_history(request):
    current_user = request.user
    tr_list_buyer = Transactions.objects.all().filter(Q(buyer=current_user.id)).order_by('-transaction_date')
    tr_list_seller = Transactions.objects.all().filter(Q(seller=current_user.id)).order_by('-transaction_date')
    return render(request, 'main/transaction_history.html', {'tr_list_buyer': tr_list_buyer,'tr_list_seller':tr_list_seller})

def admin_dashboard(request):
    tr_list = Transactions.objects.all().order_by('-transaction_date')
    return render(request,'main/admin_dashboard.html',{'tr_list':tr_list})

#def new_transaction(request):
#    if request.method == "POST":
#        form = TransactionsForm(request.POST)
#        if form.is_valid():
#            form.save()

#            # section to add in transaction into stock_price table
#            stock_date = form.cleaned_data['transaction_date']
#            stock_symbol = form.cleaned_data['stock_id']
#            stock_price = form.cleaned_data['price_per_stock']
#            stock_volume = form.cleaned_data['numstocks']

#            try:
#                stock = Stockprice.objects.get(stock_id = stock_symbol, date = stock_date)
#                if (stock.high < stock_price):
#                    stock.high = stock_price

#                if (stock.low > stock_price):
#                    stock.open_price = stock_price

#                stock.close = stock_price
#                stock.adjusted_close = stock_price
#                stock.volume = stock.volume + stock_volume

#            except ObjectDoesNotExist:
#                stock = Stockprice(stock_id = stock_symbol, date = stock_date, open_price = stock_price, high = stock_price, low = stock_price, close = stock_price, adjusted_close = stock_price, volume = stock_volume)

#            stock.save()
#            return redirect('/transaction_history')
#    else:
#        form = TransactionsForm()
#    return render(request, 'main/new_transaction.html', {'form': form})

def new_transaction(request):
    if request.method == "POST":
        form = TransactionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TransactionsForm()
    return render(request, 'main/new_transaction.html', {'form': form})


def live_stock_apple(request):
    return render(request,'main/live_stock_apple.html',{})