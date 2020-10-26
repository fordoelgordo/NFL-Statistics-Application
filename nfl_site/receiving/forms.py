from django import forms


class ReceiveForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


class TopReceiveForm(forms.Form):
    player_num = forms.IntegerField(label='Number of players')
