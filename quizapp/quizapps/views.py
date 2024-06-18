from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.

# Global Variables
score = 0


def index(request):
    quizs = Quizs.objects.all()
    context = {'quizs': quizs}
    return render(request, 'quizapps/index.html', context)


def quiz(request, quiz_id):
    quiz = Quizs.objects.get(id=quiz_id)
    questions = quiz.question_set.all()
    context = {'questions': questions}
    return render(request, 'quizapps/quiz.html', context)


def question(request, question_id):
    question = Question.objects.get(id=question_id)

    CHOICES = question.genchoiceslist()

    form = RadioChoiceForm()
    form.fields['Choice'].choices = CHOICES

    context = {'question': question, 'form': form}
    return render(request, 'quizapps/question.html', context)


def results(request, question_id):  # Maybe add quiz id of results replace to quiz id
    global score  # Must make it reset for each quiz
    choice_id = request.POST['Choice']
    choice = Choice.objects.get(id=choice_id)

    if choice.correct_choice():
        score += 1

    context = {'choice': choice}
    return render(request, 'quizapps/results.html', context)


def create_question(request):

    if request.method != 'POST':
        qz_form = QuizForm()
        q_form = QuestionForm()
        c_form = ChoiceForm()
    else:
        qz_form = QuizForm(data=request.POST)
        q_form = QuestionForm(data=request.POST)
        c_form = ChoiceForm(data=request.POST)

        if all([qz_form.is_valid(), q_form.is_valid(), c_form.is_valid()]):
            qz = qz_form.save()
            q = q_form.save(commit=False)
            c = c_form.save(commit=False)
            q.quiz = qz
            c.question = q
            q = q.save()
            c_form.save()

    context = {'qz_form': qz_form, 'q_form': q_form, 'c_form': c_form}
    return render(request, 'quizapps/create_question.html', context)
