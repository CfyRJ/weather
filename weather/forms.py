from django import forms


class PlaceForm(forms.Form):
    place = forms.CharField(label="Введите название города", max_length=100)
