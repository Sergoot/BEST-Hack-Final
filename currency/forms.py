from django import forms
from django.forms import NumberInput


class ValueForm(forms.Form):
    value = forms.FloatField(widget=NumberInput(attrs={
        'id': 'InputValue',
        'class': 'form-control',
    }))
