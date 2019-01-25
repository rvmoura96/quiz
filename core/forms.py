from django import forms


from core.models import Email


class EmailForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ['email']
