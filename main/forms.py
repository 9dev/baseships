import json
import re

from django import forms

from main.models import BOARD_SIZE, SHIPS


class NewGameForm(forms.Form):
    fields = forms.CharField(max_length=BOARD_SIZE**2, min_length=BOARD_SIZE**2, widget=forms.HiddenInput())
    ships = forms.CharField(max_length=BOARD_SIZE**2*2, widget=forms.HiddenInput())

    def clean_fields(self):
        fields = self.cleaned_data['fields']

        if not re.match('^[01]*$', fields):
            raise forms.ValidationError('Incorrect data provided!')

        if fields.count('1') < 2:
            raise forms.ValidationError('Too few ships!')

        return [fields[i:i+BOARD_SIZE] for i in range(0, BOARD_SIZE**2, BOARD_SIZE)]  # convert str to list

    def clean_ships(self):
        ships = json.loads(self.cleaned_data['ships'])

        if not isinstance(ships, list) or not isinstance(ships[0], list):
            raise forms.ValidationError('Incorrect data provided!')

        points = set(str(part) for ship in ships for part in ship)
        if len(points) != sum(SHIPS):
            raise forms.ValidationError('At least one of your ships is not completed!')

        for ship in ships:
            x = sorted(point[0] for point in ship)
            y = sorted(point[1] for point in ship)

            x_set = set(x)
            y_set = set(y)

            if len(x_set) != 1 and len(y_set) != 1:
                raise forms.ValidationError('Please draw your ships either horizontally or vertically!')

            if x != list(range(x[0], len(x) + x[0])) and y != list(range(y[0], len(y) + y[0])):
                raise forms.ValidationError('You cannot divide one big ship into several smaller ones!')

        return ships
