# Generated by Django 5.0.6 on 2024-06-18 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapps', '0004_question_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='choice_text',
            field=models.CharField(max_length=200),
        ),
    ]