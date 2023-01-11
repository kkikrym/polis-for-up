from django import forms
from .models import Stock, Trade, CURRENCY_CHOICES

class StockSearchForm(forms.Form):
    stock_id = forms.CharField(max_length=255,
                               widget= forms.TextInput(attrs={'placeholder': 'MSFT...Microsoft'}))

class WlSearchForm(forms.Form):
    stock_name = forms.CharField(max_length=255, label=None, widget= forms.TextInput(attrs={'class': 'form-control', 'id':'WlSearch',}))

class TradeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    stock_name = forms.CharField(max_length=255, label="銘柄", widget= forms.TextInput(attrs={'id':'TradeSearch',}))

    price = forms.FloatField(label="購入時株価")

    currency = forms.fields.ChoiceField(label="", choices=CURRENCY_CHOICES)

    amount = forms.IntegerField(label="数量")

    trade_date = forms.DateField(label="購入日時", widget=forms.DateInput(attrs={"type":"date"}))
