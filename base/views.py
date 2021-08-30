from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import yfinance as yf
import pandas as pd

from .forms import StockSearch

# Create your views here.


def index(request):
    form = StockSearch(request.POST)
    if request.method == "POST":
        #    stock_name = request.POST['stock_name']
        #    return redirect('stock_result',stockname=str(stock_name))

        # MODEL FORM
        if form.is_valid():
            stock_name = form.cleaned_data['stock_name']
            return redirect('stock_result', stockname=str(stock_name))

    return render(request, 'base/index.html', {'form': form})

# TODO Need complate search system in result page
# TODO Historical Data need imporve to screen roll than show data
def search_result(request, stockname):
    form = StockSearch(request.POST)

    if request.method == "GET":
        final = yf.Ticker(stockname)
        stock_price_close = []
        stock_date = []
        try:
            ### Test Use DataFrame to get info ###
            info = pd.DataFrame.from_dict(final.info, orient='index').rename(columns={0: 'value'})

            ## Check All Data ###
            info_result = pd.DataFrame(list(final.info.items()),columns=['key','value'])
            # print(info_result)

            ### Get actions ###
            actions = final.financials
            print(actions)

            ### Get Specific INFO ###
            infos = final.info
            # print(infos)

            ### Get History Data ###
            stock_price = final.history(period='5y') # Get 10 year data
            stock_price.reset_index(inplace=True) # Make "Date" become columns

            ### Data Format ###
            stock_price['Date'] = stock_price['Date'].dt.strftime('%Y-%m-%d')
            stock_price['Open'] = stock_price['Open'].round(2)
            stock_price['High'] = stock_price['High'].round(2)
            stock_price['Low'] = stock_price['Low'].round(2)
            stock_price['Close'] = stock_price['Close'].round(2)

            stock_price_all = stock_price.copy().iloc[::-1]

            ### Currently need data ###
            for date, close in zip(stock_price['Date'], stock_price['Close']):
                stock_price_close.append(close)
                stock_date.append(date) # get Y-M-D

            
            return render(request, 'base/stock_result.html', {'stockname': stockname, 'infos': infos, 'stock_price': stock_price_close, 'stock_date': stock_date, 'form': form, 'stock_price_all': stock_price_all})
        except ValueError as error:
            return HttpResponse('<h1>{} Not Found</h1>'.format(stockname))

    if request.method == "POST":
        
        if form.is_valid():
            stock_name = form.cleaned_data['stock_name']
            print(stock_name)
            
            return redirect('stock_result', stockname=str(stock_name))
        else:
            return HttpResponse('<h1>{} Not Found</h1>'.format(stockname))
