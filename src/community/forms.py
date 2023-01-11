from django import forms
from .models import Community
from django_summernote.widgets import SummernoteWidget
from django_summernote.fields import SummernoteTextFormField

class CommunityCreateForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ['community_name', 'description', 'category',]
        widgets = {
            'community_name': forms.TextInput(
                    attrs={
                        'class': 'form-control'
                    }
                ),
            'description': forms.Textarea(
                    attrs={
                        'class': 'form-control'
                    }
                )
        }

