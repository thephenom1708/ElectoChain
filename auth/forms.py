from django import forms
from .models import Voter, ActiveVoter, Admin

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Admin
        fields = ['thumb_id', 'password']


