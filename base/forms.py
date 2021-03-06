from django import forms

class StockSearch(forms.Form):
    Stock_name = forms.CharField()