from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number']
        widgets = {
            'table_number': forms.NumberInput(attrs={
                'min': 1, "max": 25, 'style': "width: 50px"
            }),
        }
        labels = {
            'table_number': "Номер стола",
        }

