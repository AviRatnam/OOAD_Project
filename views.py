from django.shortcuts import render, redirect, HttpResponse
from .forms import StocksymbolForm, StockpriceForm, TransactionsForm
from .models import Transactions
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


from .models import Stockprice

#---- Live stocks

import math
import pandas_datareader as web
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
from datetime import date
from datetime import timedelta
import plotly.graph_objects as go
from plotly.offline import plot

#---- |


def prediction(df):
    #cell1----------
    
    #creating new dataframe with 'close' column
    data = df.filter(['Close'])
    dataset = data.values
    #rows to train
    training_data_len = math.ceil(len(dataset) * .8)
    training_data_len
    
    #cell2----------

    #scaling the data

    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    #cell3----------

    #creating test and training dataset3

    train_data = scaled_data[0:training_data_len, :]

    #splitting into x_train and y_train sets

    x_train = []
    y_train = []

    for i in range (60,len(train_data)):
        x_train.append(train_data[i-60:i,0])
        y_train.append(train_data[i,0])

    #cell4----------
    
    x_train, y_train = np.array(x_train), np.array(y_train)
    
    #cell5----------

    x_train = np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))

    #cell6----------

    #building lSTM model
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1],1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    
    #cell7----------

    model.compile(optimizer='adam', loss='mean_squared_error')

    #cell8----------

    model.fit(x_train, y_train, batch_size=1, epochs=1) 

    #cell9----------

    #creating testing data set9

    test_data = scaled_data[training_data_len - 60: , :]

    x_test = []
    y_test = dataset[training_data_len:, :]

    for i in range (60, len(test_data)):
        x_test.append(test_data[i-60:i,0])

    #cell10----------
    #convert to numpy array10
    x_test = np.array(x_test)
    #cell11----------
    #reshape the data11
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1],1))
    #cell12----------
    #get the model predicted price values12

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    #cell13----------
    #finding the root mean squared error

    rmse = np.sqrt(np.mean(predictions - y_test)**2)

    #------
    #plot the data
    train = data[:training_data_len]
    valid = data[training_data_len:].copy()
    valid['Predictions'] = predictions
    print("reached the end predicted.")

    #visualise 
    '''
    plt.figure(figsize=(16,8))
    plt.title('Model')
    plt.xlabel('Data',fontsize=18)
    plt.ylabel('Close Price USD',fontsize=18)
    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    plt.legend(['Train','Val','Prections'],loc='lower right')
    figure=plot(plt.show(),output_type='div')
    '''
    #train_u.columns
    import plotly.express as px
    fig= px.line(valid,x=df[training_data_len:]['Date'],y='Predictions')
    fig.write_html("main/lala.html")
    print("fig created")
    print(valid)
    figure=plot(fig,auto_open=False,output_type='div')
    return figure

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

def search_stocks(request):
    
    

    if request.method == 'POST':
        stockname=request.POST.get('textfield',None)
        try:
            comp = stockname
            df = web.DataReader(comp, data_source='yahoo', start='2012-01-01', end=date.today())
            minVal = df.min()
            maxVal = df.max()
            training_data_len = math.ceil(len(df) * .8)
            print("History of Minimum Values")
            print(minVal.round(2))
            print("History of Maximum Values")
            print(maxVal.round(2))
            print(df)
            #
            df.reset_index(inplace=True,drop=False)
            candleStickFig = go.Figure(data=[go.Candlestick(
                            x=df[:training_data_len]['Date'],
                            open=df[:training_data_len]['Open'],
                            high=df[:training_data_len]['High'],
                            low=df[:training_data_len]['Low'],
                            close=df[:training_data_len]['Close'])
                            ])
            #candleStickFig.update_layout(xaxis_rangeslider_visible=False)
            #candleStickFig.show()
            candlestick_div=plot(candleStickFig,output_type='div')
            figure=prediction(df)
            return render(request,'main/live_stocks.html',{'name':stockname,'candlestick':candlestick_div,'figure':figure})
            #
        except:
            return HttpResponse("No such stock")
    else:
        return render(request,'main/test.html')

#shows top 3 companies on NASDAQ as default and gives option to search specific stock
def live_stocks(request):
    return render(request,'main/test.html')
 
'''
def live_stocks(request):
    #code to fetch data
    #getting stock quote
    comp = 'TSLA'
    df = web.DataReader(comp, data_source='yahoo', start='2012-01-01', end=date.today())
    minVal = df.min()
    maxVal = df.max()

    print("History of Minimum Values")
    print(minVal.round(2))
    print("History of Maximum Values")
    print(maxVal.round(2))
    print(df)

    #
    df.reset_index(inplace=True,drop=False)
    candleStickFig = go.Figure(data=[go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])
                    ])
    #candleStickFig.update_layout(xaxis_rangeslider_visible=False)
    #candleStickFig.show()
    candlestick_div=plot(candleStickFig,output_type='div')
    #
    return render(request,'main/test.html',{'candlestick':candlestick_div})
'''

def user_profile(request):
    return render(request,'main/user_profile.html',{})

'''old
def transaction_history(request):
    current_user = request.user
    tr_list_buyer = Transactions.objects.all().filter(Q(buyer=current_user.id)).order_by('-transaction_date')
    tr_list_seller = Transactions.objects.all().filter(Q(seller=current_user.id)).order_by('-transaction_date')
    return render(request, 'main/transaction_history.html', {'tr_list_buyer': tr_list_buyer,'tr_list_seller':tr_list_seller})
'''
def transaction_history(request):
    current_user = request.user
    tr_list_buyer = Transactions.objects.all().filter(Q(user=current_user.id) | Q(type_transaction = 'buyer')).order_by('-transaction_date')
    tr_list_seller = Transactions.objects.all().filter(Q(user=current_user.id)| Q(type_transaction = 'seller')).order_by('-transaction_date')
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
'''old
def new_transaction(request):
    if request.method == "POST":
        form = TransactionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TransactionsForm()
    return render(request, 'main/new_transaction.html', {'form': form})
'''

def live_stock_apple(request):
    return render(request,'main/live_stock_apple.html',{})

def new_transaction(request):
    if request.method == "POST":
        form = TransactionsForm(request.POST)
        if form.is_valid():
            form.save()

            # section to add in transaction into stock_price table
            stock_date = form.cleaned_data['transaction_date']
            stock_symbol = form.cleaned_data['stock_id']
            stock_price = form.cleaned_data['price_per_stock']
            stock_volume = form.cleaned_data['numstocks']

            try:
                stock = Stockprice.objects.get(stock_id = stock_symbol, date = stock_date)
                if (stock.high < stock_price):
                    stock.high = stock_price

                if (stock.low > stock_price):
                    stock.open_price = stock_price

                stock.close_price = stock_price
                stock.adjusted_close = stock_price
                stock.volume = stock.volume + stock_volume

            except ObjectDoesNotExist:
                stock = Stockprice(stock_id = stock_symbol, date = stock_date, open_price = stock_price, high = stock_price, low = stock_price, close_price = stock_price, adjusted_close = stock_price, volume = stock_volume)

            stock.save()
            return redirect('/transaction_history')
    else:
        form = TransactionsForm()
    return render(request, 'main/new_transaction.html', {'form': form})

def stock_history(request):
    stock_list = Stockprice.objects.all().order_by('-date')
    return render(request,'main/stock_history.html',{'stock_list':stock_list})