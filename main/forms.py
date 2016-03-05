import re

from django import forms

from main.models import BOARD_SIZE


class NewGameForm(forms.Form):
    fields = forms.CharField(max_length=BOARD_SIZE**2, min_length=BOARD_SIZE**2, widget=forms.HiddenInput(), label="Board")

    def clean_fields(self):
        fields = self.cleaned_data['fields']

        if not re.match('^[01]*$', fields):
            raise forms.ValidationError('Incorrect data provided!')

        if fields.count('1') < 2:
            raise forms.ValidationError('Too few ships!')

        return [fields[i:i+BOARD_SIZE] for i in range(0, BOARD_SIZE**2, BOARD_SIZE)]  # convert str to list
