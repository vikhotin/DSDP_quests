from django.forms import ModelForm
from .models import Quest


class QuestForm(ModelForm):
    class Meta:
        model = Quest
        fields = ['user_id', 'places_ids', 'puzzles_ids', 'cur_task', 'completed']
