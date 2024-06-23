from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
# Create your views here.

# Global Variables
score = 0


def index(request):
    global score
    score = 0
    quizs = Quizs.objects.filter(owner=request.user.id)
    user = request.user
    context = {'quizs': quizs, 'user': user}
    return render(request, 'quizapps/index.html', context)


@login_required
def quiz(request, quiz_id):
    quiz = Quizs.objects.get(id=quiz_id)
    if request.user not in quiz.owner.all():
        raise Http404
    questions = quiz.question_set.all()
    context = {'questions': questions, 'quiz': quiz}
    return render(request, 'quizapps/quiz.html', context)


@login_required
def question(request, question_id):
    question = Question.objects.get(id=question_id)

    if request.user not in question.quiz.owner.all():
        raise Http404

    CHOICES = question.genchoiceslist()

    form = RadioChoiceForm()
    form.fields['Choice'].choices = CHOICES

    context = {'question': question, 'form': form}
    return render(request, 'quizapps/question.html', context)


@login_required
def results(request, question_id):  # Maybe add quiz id of results replace to quiz id
    global score
    choice_id = request.POST['Choice']
    choice = Choice.objects.get(id=choice_id)
    totalquestions = len(list(Question.objects.get(id=question_id).quiz.question_set.all()))
    question = Question.objects.get(id=question_id)

    if choice.correct_choice:
        score += 1

    context = {'choice': choice, 'score': score, 'totalquestions': totalquestions}
    if question.isnotlastquestion() == True:
        return redirect('quizapps:question', question.returnnextquestionid())
    else:
        return redirect('quizapps:resultsquiz', question.quiz.id)


@login_required
def resultsquiz(request, quiz_id):
    global score
    quiz = Quizs.objects.get(id=quiz_id)
    totalquestions = len(list(quiz.question_set.all()))
    score_set = str(score)+"/"+str(totalquestions)

    if request.user.userprofile.role == "ST":
        score_obj = Score.objects.create(owner=request.user, quiz=quiz, score=score_set)
        quiz.owner.remove(request.user)
        score_obj.save()

    context = {'score': score, 'totalquestions': totalquestions}
    return render(request, 'quizapps/resultsquiz.html', context)


@login_required
def create_quiz(request):
    if request.user.userprofile.role == "TR":
        if request.method != 'POST':
            form = QuizForm()
        else:
            form = QuizForm(data=request.POST)
            if form.is_valid():
                q_form = form.save(commit=False)
                form.save()  # This creates the object without user
                form.save_m2m()
                q_form.owner.add(request.user)
                q_form.save()
            return redirect('quizapps:index')
        context = {'form': form}
        return render(request, 'quizapps/create_quiz.html', context)
    else:
        return HttpResponse("No Student Can Create Quiz!")


@login_required
def create_question(request, quiz_id):
    if request.user.userprofile.role == "TR":
        quiz = Quizs.objects.get(id=quiz_id)
        ChoiceFormSet = modelformset_factory(
            Choice, fields=('choice_text', 'correct_choice'), extra=4)

        if request.user not in quiz.owner.all():
            raise Http404

        if request.method != 'POST':
            q_form = QuestionForm()
            c_form = ChoiceFormSet(queryset=Choice.objects.none())
        else:
            q_form = QuestionForm(data=request.POST)
            c_form = ChoiceFormSet(data=request.POST)

            if all([q_form.is_valid(), c_form.is_valid()]):
                q = q_form.save(commit=False)
                c = c_form.save(commit=False)
                # Assigning Quiz to Question
                q.quiz = Quizs.objects.get(id=quiz_id)
                # non commit false returns None
                q.save()  # save the non commit instance not the form
                for form in c:
                    form.question = q
                    form.save()
                return redirect('quizapps:quiz', quiz_id)
        context = {'q_form': q_form, 'c_form': c_form, 'quiz': quiz}
        return render(request, 'quizapps/create_question.html', context)

    else:
        return HttpResponse("No Student Can Create Question!")


@login_required
def edit_question(request, question_id):
    if request.user.userprofile.role == "TR":
        question = Question.objects.get(id=question_id)
        ChoiceFormSet = modelformset_factory(Choice, fields=(
            'choice_text', 'correct_choice'), extra=4, max_num=4)

        if request.user not in question.quiz.owner.all():
            raise Http404

        if request.method != 'POST':
            q_form = QuestionForm(instance=question)
            c_form = ChoiceFormSet(queryset=Choice.objects.filter(question=question))
            # for edit use queryset such that it filters to the question__id = questoin.id
        else:
            q_form = QuestionForm(data=request.POST, instance=question)
            c_form = ChoiceFormSet(
                data=request.POST, queryset=Choice.objects.filter(question=question))
            if all([q_form.is_valid(), c_form.is_valid()]):
                q = q_form.save(commit=False)
                c = c_form.save(commit=False)
                q.save()
                for form in c:
                    form.question = q
                    form.save()
                return redirect('quizapps:quizview', question.quiz.id)
        context = {'q_form': q_form, 'c_form': c_form, 'question': question}
        return render(request, 'quizapps/edit_question.html', context)
    else:
        return HttpResponse("No Student Can Edit Question!")


@login_required
def quizview(request, quiz_id):
    quiz = Quizs.objects.get(id=quiz_id)

    if request.user not in quiz.owner.all():
        raise Http404

    questions = quiz.question_set.all()
    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'quizapps/quizview.html', context)


@login_required
def delete_question(request, question_id):
    if request.user.userprofile.role == "TR":
        question = Question.objects.get(id=question_id)

        if request.user not in question.quiz.owner.all():
            raise Http404

        question.delete()
        return redirect('quizapps:quizview', question.quiz.id)
    else:
        return HttpResponse("No Student Can Delete Question!")


@login_required
def delete_quiz(request, quiz_id):
    if request.user.userprofile.role == "TR":
        quiz = Quizs.objects.get(id=quiz_id)

        if request.user not in quiz.owner.all():
            raise Http404

        quiz.delete()
        return redirect('quizapps:index')
    else:
        return HttpResponse("No Student Can Delete Quiz!")


@login_required
def assign_quiz(request, quiz_id):
    if request.user.userprofile.role == "TR":
        quiz = Quizs.objects.get(id=quiz_id)

        # Genrating Users
        CHOICES = []
        for user in User.objects.all():
            if user.userprofile.role == "ST":
                if user not in quiz.owner.all():
                    CHOICES.append((user.id, user))

        if request.user not in quiz.owner.all():
            raise Http404

        if request.method != 'POST':
            form = MultipleUserForm()
            form.fields['MultipleUser'].choices = CHOICES
        else:
            form = MultipleUserForm()
            form.fields['MultipleUser'].choices = CHOICES
            print(request.POST)
            print(request.POST['MultipleUser'])
            for id in dict(request.POST)['MultipleUser']:  # requires more than one user
                quiz.owner.add(User.objects.get(id=id))
                quiz.save()
            return redirect('quizapps:quiz', quiz.id)

        context = {'form': form, 'quiz': quiz}
        return render(request, 'quizapps/assign_quiz.html', context)
    else:
        return HttpResponse("No Student Can Assign Quiz!")


@login_required
def reportcard(request):
    if request.user.userprofile.role == "ST":
        scores = Score.objects.filter(owner=request.user)
        context = {'scores': scores}
        return render(request, 'quizapps/reportcard.html', context)
    else:
        scores = []
        user_list = []
        for score in Score.objects.all():
            for owner in score.quiz.owner.all():
                if owner == request.user:
                    scores.append(score)
        user = request.user
        for score in scores:
            user_list.append(score.owner)
        user_list = list(set(user_list))  # Make the list unique
        context = {'scores': scores, 'user': user, 'user_list': user_list}
        return render(request, 'quizapps/reportcard.html', context)
