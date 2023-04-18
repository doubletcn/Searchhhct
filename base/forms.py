from django import forms
from .models import Task
# Reordering Form and View


class PositionForm(forms.Form):
    position = forms.CharField()


class ClothingFilterForm(forms.Form):
    tags = forms.MultipleChoiceField(choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].choices = Task.objects.all().values_list('tags', 'tags').distinct()
