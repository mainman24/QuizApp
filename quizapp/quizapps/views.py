from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


def index(request):
    questions = Question.objects.all()
    context = {'questions': questions}
    return render(request, 'quizapps/index.html', context)


def question(request, question_id):
    question = Question.objects.get(id=question_id)
    print(question.isnotlastquestion())
    CHOICES = []
    for choice in question.choice_set.all():
        CHOICES.append((choice.id, choice.choice_text))

    form = RadioChoiceForm()
    form.fields['Choice'].choices = CHOICES

    context = {'question': question, 'form': form}
    return render(request, 'quizapps/question.html', context)


def results(request, question_id):  # Maybe add quiz id of results replace to quiz id
    choice_id = request.POST['Choice']
    choice = Choice.objects.get(id=choice_id)
    print(choice.correct_choice)
    context = {'choice': choice}
    return render(request, 'quizapps/results.html', context)
