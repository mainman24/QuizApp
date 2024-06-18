from django import forms
from .models import *


class RadioChoiceForm(forms.Form):
    Choice = forms.ChoiceField(widget=forms.RadioSelect())


# see form in django
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quizs
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_name"]


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["choice_text"]
