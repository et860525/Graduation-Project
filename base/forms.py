from django import forms

class StockSearch(forms.Form):
    error_css_class = 'error'
    stock_name = forms.CharField(label=False, max_length='50', required = False)
    stock_name.widget.attrs.update({'class': "form-control"})
