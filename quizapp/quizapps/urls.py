from django.urls import path

from . import views

app_name = 'quizapps'

urlpatterns = [
    path('', views.index, name="index"),
    path('quiz/<int:quiz_id>', views.quiz, name="quiz"),
    path('question/<int:question_id>', views.question, name="question"),
    path('results/<int:question_id>', views.results, name="results"),
    path('create_question/<int:quiz_id>', views.create_question, name="create_question"),
    path('edit_question/<int:question_id>', views.edit_question, name="edit_question"),
    path('create_quiz/', views.create_quiz, name="create_quiz"),
    path('quizview/<int:quiz_id>', views.quizview, name="quizview"),
]
