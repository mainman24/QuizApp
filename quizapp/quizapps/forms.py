from django import forms


class RadioChoiceForm(forms.Form):
    Choice = forms.ChoiceField(widget=forms.RadioSelect())
