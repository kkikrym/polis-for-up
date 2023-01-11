from django import forms
from .models import Team, TeamArticle, TeamThread
from stock.models import Stock
from django_summernote.widgets import SummernoteWidget
from django_summernote.fields import SummernoteTextFormField
from .models import CATEGORIES

class TeamChangeForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'description']


class TeamArticleCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = 0
    class Meta:
        model = TeamArticle
        fields = ['title','category', 'thumbnail','content', 'is_published']
        widgets = {
            'content':SummernoteWidget(),
            #'thumbnail': forms.FileInput,
            #'category':forms.ChoiceField(choices=CATEGORIES, widget=forms.ChoiceField(attrs={'class':'form-contr'}))
        }
        initial = {
            'category':'0',
        }


class ChatMessageForm(forms.Form):
    chatbox = SummernoteTextFormField()

class ThreadCreateForm(forms.ModelForm):
    class Meta:
        model = TeamThread
        fields = ['thread_name']
        widgets = {
            'thread_name': forms.TextInput(attrs={'class': 'form-control'},)
        }

class TeamChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Team
        fields = ['team_name', 'description', ]
