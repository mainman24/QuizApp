from django.urls import path

from . import views

app_name = 'quizapps'

urlpatterns = [
    path('', views.index, name="index"),
    path('quiz/<int:quiz_id>', views.quiz, name="quiz"),
    path('question/<int:question_id>', views.question, name="question"),
    path('results/<int:question_id>', views.results, name="results"),
    path('create_question/', views.create_question, name="create_question")
]
