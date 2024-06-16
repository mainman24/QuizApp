from django.db import models

# Create your models here.


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quiz_name


class Question(models.Model):
    quiz = models.ForeignKey(quiz, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_name

    def isnotlastquestion(self):
        if self.id == len(Question.objects.all()):
            return False
        else:
            return True


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    correct_choice = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
