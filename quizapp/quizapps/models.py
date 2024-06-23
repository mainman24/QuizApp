from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Quizs(models.Model):
    owner = models.ManyToManyField(User)
    quiz_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def createquizfromdict(self, dict):
        for i in dict:
            q = Question.objects.create(quiz=self, question_name=i)
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

    def __str__(self):
        return self.question_name

    def returnnextquestionid(self):
        questions = list(self.quiz.question_set.all())
        question_id = questions.index(self)
        return questions[question_id + 1].id

    def genchoiceslist(self):
        CHOICES = []
        for choice in self.choice_set.all():
            CHOICES.append((choice.id, choice.choice_text))
        return CHOICES

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

    def __str__(self):
        return self.choice_text


class UserProfile(models.Model):
    CHOICES = [
        ("TR", "Teacher"),
        ("ST", "Student")
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200, choices=CHOICES)

    def __str__(self):
        return str(self.owner) + "," + str(self.role)


class Score(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizs, on_delete=models.CASCADE)
    score = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.owner) + "," + str(self.quiz) + "," + str(self.score)
