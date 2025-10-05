from django import forms
from .models import *

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class SelectPCForm(forms.Form):
    pc = forms.ModelChoiceField(
        queryset=ComputerList.objects.filter(is_active=False), 
        empty_label="Select a PC"
    )