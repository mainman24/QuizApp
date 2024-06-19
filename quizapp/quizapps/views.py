from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import modelformset_factory
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
    context = {'questions': questions, 'quiz': quiz}
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

    # if choice.correct_choice():
    #    score += 1

    context = {'choice': choice}
    return render(request, 'quizapps/results.html', context)

# create a view for making questions


def create_quiz(request):
    if request.method != 'POST':
        form = QuizForm()
    else:
        form = QuizForm(data=request.POST)
        if form.is_valid():
            form.save()
        return redirect('quizapps:index')
    context = {'form': form}
    return render(request, 'quizapps/create_quiz.html', context)


def create_question(request, quiz_id):  # Maybe make it such that it is for a quiz
    ChoiceFormSet = modelformset_factory(Choice, fields=('choice_text', 'correct_choice'), extra=4)
    if request.method != 'POST':
        #qz_form = QuizForm()
        q_form = QuestionForm()
        c_form = ChoiceFormSet(queryset=Choice.objects.none())
        # for edit use queryset such that it filters to the question__id = questoin.id
    else:
        #qz_form = QuizForm(data=request.POST)
        q_form = QuestionForm(data=request.POST)
        c_form = ChoiceFormSet(data=request.POST)

        # if all([qz_form.is_valid(), q_form.is_valid(), c_form.is_valid()]):
        if all([q_form.is_valid(), c_form.is_valid()]):
            #qz = qz_form.save()
            q = q_form.save(commit=False)
            c = c_form.save(commit=False)
            q.quiz = Quizs.objects.get(id=quiz_id)
            print(c)
            q.save()
            for form in c:
                #print(instance.question, q)
                # print(form)
                form.question = q
                form.save()
            return redirect('quizapps:quiz', quiz_id)

            # c_form.save()
    quiz = Quizs.objects.get(id=quiz_id)
    #context = {'qz_form': qz_form, 'q_form': q_form, 'c_form': c_form}
    context = {'q_form': q_form, 'c_form': c_form, 'quiz': quiz}
    return render(request, 'quizapps/create_question.html', context)


def edit_question(request, question_id):  # Maybe make it such that it is for a quiz
    question = Question.objects.get(id=question_id)
    ChoiceFormSet = modelformset_factory(Choice, fields=(
        'choice_text', 'correct_choice'), extra=4, max_num=4)
    if request.method != 'POST':
        #qz_form = QuizForm()
        q_form = QuestionForm(instance=question)
        c_form = ChoiceFormSet(queryset=Choice.objects.filter(question=question))
        # for edit use queryset such that it filters to the question__id = questoin.id
    else:
        #qz_form = QuizForm(data=request.POST)
        q_form = QuestionForm(data=request.POST, instance=question)
        c_form = ChoiceFormSet(data=request.POST, queryset=Choice.objects.filter(question=question))

        # if all([qz_form.is_valid(), q_form.is_valid(), c_form.is_valid()]):
        if all([q_form.is_valid(), c_form.is_valid()]):
            #qz = qz_form.save()
            q = q_form.save(commit=False)
            c = c_form.save(commit=False)
            #q.quiz = Quizs.objects.get(id=quiz_id)
            # print(c)
            q.save()
            for form in c:
                #print(instance.question, q)
                # print(form)
                form.question = q
                form.save()
            return redirect('quizapps:quizview', question.quiz.id)

            # c_form.save()
    #quiz = Quizs.objects.get(id=quiz_id)
    #context = {'qz_form': qz_form, 'q_form': q_form, 'c_form': c_form}
    context = {'q_form': q_form, 'c_form': c_form, 'question': question}
    return render(request, 'quizapps/edit_question.html', context)


def quizview(request, quiz_id):
    quiz = Quizs.objects.get(id=quiz_id)
    questions = quiz.question_set.all()
    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'quizapps/quizview.html', context)
