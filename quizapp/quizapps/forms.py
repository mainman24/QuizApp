from django import forms
from .models import *


class RadioChoiceForm(forms.Form):
    Choice = forms.ChoiceField(widget=forms.RadioSelect(), label=False)  # label = False


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quizs
        fields = ['quiz_name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["question_name"]


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["choice_text"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["role"]


class MultipleUserForm(forms.Form):
    MultipleUser = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label=False)
