from django import forms
from .models import *


class RadioChoiceForm(forms.Form):
    Choice = forms.ChoiceField(widget=forms.RadioSelect(), label=False)  # label = False


# see form in django
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quizs
        fields = '__all__'  # change to only quiz_name


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
        fields = ["role"]  # Change to only form

# class MultipleUserForm():


class MultipleUserForm(forms.Form):
    MultipleUser = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(), label=False)
