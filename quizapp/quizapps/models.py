from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# question.id|add:'1'


class Quizs(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
# maybe add score to Quizs
# {'question_name':[('Choice1', False) , ('Choice2', True) , ('Choice3', False) , (Choice4, False)]}

    def createquizfromdict(self, dict):
        for i in dict:
            q = Question.objects.create(quiz=self, question_name=i)
            #q.quiz_id = self.id
            q.save()
            for j in dict[i]:
                c = Choice.objects.create(question=q, choice_text=j[0])
                if j[1] == True:
                    c.correct_choice = True
                c.question = q
                c.save()

    def __str__(self):
        return self.quiz_name


class Question(models.Model):
    quiz = models.ForeignKey(Quizs, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
# add choices field to Question
# maybe use this
# https://docs.djangoproject.com/en/5.0/topics/db/models/#field-options

    def __str__(self):
        return self.question_name

    def returnnextquestionid(self):
        questions = list(self.quiz.question_set.all())
        question_id = questions.index(self)
        # if Question.objects.get(id=question_id) != questions[-1]:
        # maybe remove this
        return questions[question_id + 1].id

    def genchoiceslist(self):
        CHOICES = []
        for choice in self.choice_set.all():
            CHOICES.append((choice.id, choice.choice_text))
        return CHOICES

# Fix this function Done
    def isnotlastquestion(self):
        questions = list(self.quiz.question_set.all())
        question_id = questions.index(self)
        if self == questions[-1]:
            return False
        else:
            return True

    def returncurrentid(self):
        questions = list(self.quiz.question_set.all())
        question_id = questions.index(self)
        return question_id + 1


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    correct_choice = models.BooleanField(default=False)
#    marks = models.IntegerField the marks to be added if correct

    def __str__(self):
        return self.choice_text


class UserProfile(models.Model):
    CHOICES = [
        ("TR", "Teacher"),
        ("ST", "Student")
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200, choices=CHOICES)

    def __str__(self):
        return self.owner + " , " + self.role
