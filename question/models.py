from django.db import models
from category.models import Category
from user.models import CustomUser


class StateChoices(models.TextChoices):
    ACCEPT = ('accept', 'Accept')
    FAILED = ('failed', 'Failed')
    PENDING = ('pending', 'Pending')


class Question(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, name='category')
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, name='user')
    text = models.CharField(max_length=250)
    correct_answer = models.CharField(max_length=250)
    mistake_answer_1 = models.CharField(max_length=250)
    mistake_answer_2 = models.CharField(max_length=250)
    mistake_answer_3 = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(
        max_length=10, choices=StateChoices.choices, default='pending')

    def __str__(self) -> str:
        return self.text


class ReportChoices(models.TextChoices):
    NONE = ('None', 'None')
    BAD_QUESTION = ('bad_question', "That's bad question.")
    GOOD_QUESTION = ('good_question', "That's good question.")
    NO_IDEA = ('no_idea', "I don't have idea.")


class ReportQuestion(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, null=True)
    report = models.CharField(
        max_length=25, choices=ReportChoices.choices, default='None')

    def __str__(self) -> str:
        return self.question.text
