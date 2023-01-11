from django import forms
from accounts.models import CustomUser
from team.models import Team
from django_summernote.widgets import SummernoteWidget
from django_summernote.fields import SummernoteTextFormField

class TeamCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta:
        model = Team
        fields = ['team_name']

class UserChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control mt-2 mb-4"
        for name in ["username", "email"]:
            self.fields[name].help_text=None
        self.fields["profile_image"].onchange = "imgPreView(event);"

    profile_image = forms.ImageField(widget=forms.FileInput)

    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'profile_message',
            'profile_image',
        ]
        labels = {
            'email':'メールアドレス',
            'profile_message':'自己紹介',
            'profile_image':'プロフィール画像',
        }