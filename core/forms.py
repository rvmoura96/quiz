from django import forms


from core.models import Email


class EmailForm(forms.Form):
    email = forms.EmailField()
    questionario = forms.HiddenInput()
    
