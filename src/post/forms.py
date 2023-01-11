from django import forms
from .models import Post
from stock.models import Stock
from django_summernote.widgets import SummernoteWidget

class PostCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = 0

    class Meta:
        model = Post
        fields = ['title','category', 'thumbnail','content', 'is_published']
        widgets = {
            'content':SummernoteWidget(),
            #'thumbnail': forms.FileInput,
            #'category':forms.ChoiceField(choices=CATEGORIES, widget=forms.ChoiceField(attrs={'class':'form-contr'}))
        }