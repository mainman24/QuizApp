# Generated by Django 5.0.6 on 2024-06-16 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapps', '0003_quizs'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='quizapps.quizs'),
            preserve_default=False,
        ),
    ]
