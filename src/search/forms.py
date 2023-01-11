from django import forms
from stock.models import Stock
from django_summernote.widgets import SummernoteWidget

class SearchForm(forms.Form):
    search = forms.CharField(max_length=255)