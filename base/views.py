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
            return redirect('stock_result',stockname=str(stock_name))
        
    return render(request, 'base/index.html', {'form': form})

def search_result(request, stockname):
    # MODEL FORM
    #if request.method == 'GET':
        #form = StockSearch(request.POST)#
        #if form.is_valid():
        #    text = form.cleaned_data['Stock_name']
        #    final = yf.Ticker(text)
        #    rs = final.info
        #    print(pd.DataFrame(list(rs.items()),columns=['key','value']))
        
    if request.method == "GET":
        final = yf.Ticker(stockname)   
        stock_price_close = []
        stock_date = []
        try:
            ### Test Use DataFrame to get info ###
            #info = pd.DataFrame.from_dict(final.info, orient='index').rename(columns={0: 'value'})

            ### Check All Data ###
            #info_result = pd.DataFrame(list(final.info.items()),columns=['key','value'])
            #print(info_result)
            
            ### Get Specific INFO ###
            infos = final.info
            #print(infos)

            info_result = {'shortName': infos['shortName'], 'country': infos['country'], 
                    'city': infos['city'], 'address1': infos['address1'], 'industry': infos['industry'],
                    'longBusinessSummary': infos['longBusinessSummary']}
            #print(info_result)

            ### Get History Data ###
            stock_price = final.history(period='5y') # Get 10 year data
            stock_price.reset_index(inplace=True) # Make "Date" become columns
            
            ### Currently need data ###
            for date, close in zip(stock_price['Date'], stock_price['Close']):
                stock_price_close.append(close) 
                stock_date.append(str(date)[:10])
            
            ### TODO Add condition to check what data show ###
            ### Show 5 YEARs ###
            stock_date = [ ele[:9] for ele in stock_date ]
            stock_date = sorted(list(set(stock_date)))
            stock_5y_mean = []
            
            #print(stock_price['Date'])
            for year in stock_date:
                stock_5y_mean.append(stock_price[stock_price['Date'].astype(str).str.contains(year)]['Close'].mean())

            print(stock_date)    
            print(stock_5y_mean)

            return render(request, 'base/stock_result.html', {'stockname': stockname, 'info_result': info_result
                                                            , 'stock_price': stock_5y_mean, 'stock_date': stock_date})
        except ValueError as error:
            return HttpResponse('<h1>{} Not Found</h1>'.format(stockname))
    return HttpResponse('<h1>Nothing</h1>')
    #return render(request, 'base/stock_result.html', {'stockname': stockname})