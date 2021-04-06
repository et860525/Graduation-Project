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
        try:
            info_result = pd.DataFrame(list(final.info.items()),columns=['key','value'])
            print(info_result)
            return render(request, 'base/stock_result.html', {'info_result': info_result})
        except ValueError as error:
            return HttpResponse('<h1>{} Not Found</h1>'.format(stockname))

        return HttpResponse('<h1>We got {} GET</h1>'.format(stockname))
    return HttpResponse('<h1>Nothing</h1>')
    #return render(request, 'base/stock_result.html', {'stockname': stockname})