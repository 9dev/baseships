from django import forms

from main.models import BOARD_SIZE


class NewGameForm(forms.Form):
    fields = forms.CharField(max_length=BOARD_SIZE**2, widget=forms.HiddenInput(), initial='0000')

    def clean_fields(self):
        fields = self.cleaned_data['fields']
        if not fields.isdigit():
            raise forms.ValidationError('Incorrect data provided!')

        return [[fields[i+j] for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]  # convert str to list
