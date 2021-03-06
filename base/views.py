from django.shortcuts import render, redirect
from base.forms import StockSearch

# Create your views here.
def index(request):
    form = StockSearch()

    if request.method == 'POST':
        form = StockSearch(request.POST)
        if form.is_valid():
            text = form.cleaned_data['Stock_name']
            print(text)
        return redirect("index")

    context = {'form': form}
    return render(request, 'base/index.html', context)