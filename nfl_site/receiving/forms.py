from django import forms


class ReceiveForm(forms.Form):
    player_name = forms.CharField(max_length=100)