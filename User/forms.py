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

class AddMoneyForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        label="Số tiền muốn nạp (đ)",
        widget=forms.NumberInput(attrs={'placeholder': 'Nhập số tiền'})
    )
