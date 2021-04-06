from django import forms

class StockSearch(forms.Form):
    error_css_class = 'error'
    stock_name = forms.CharField(label='Stock name:', max_length='50')