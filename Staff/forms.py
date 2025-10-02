from django import forms
from User.models import *

class AddComputerTypeForm(forms.ModelForm):
    class Meta:
        model = ComputerType
        fields = ['name', 'status', 'price_per_hour', 'graphics_card', 'ram', 'cpu', 'storage']

class EditComputerTypeForm(forms.ModelForm):
    class Meta:
        model = ComputerType
        fields = ['name', 'status', 'price_per_hour', 'graphics_card', 'ram', 'cpu', 'storage', 'description']

class AddComputerListForm(forms.ModelForm):
    class Meta:
        model = ComputerList
        fields = ['name', 'computer_type', 'is_active']