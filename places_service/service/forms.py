from django.forms import ModelForm
from .models import Place, Fact, Puzzle


class PlaceForm(ModelForm):
    class Meta:
        model = Place
        fields = ['name', 'long', 'lat']


class FactForm(ModelForm):
    class Meta:
        model = Fact
        fields = ['place', 'text', 'is_moderated']


class PuzzleForm(ModelForm):
    class Meta:
        model = Puzzle
        fields = ['place', 'text', 'answer', 'is_moderated']
