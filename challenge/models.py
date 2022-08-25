from django.db import models
from account.models import Account
from category.models import Category
from question.models import Question


class ChallengeRequest(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='ChallengeReq_account')
    accepted_by = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True, related_name='ChallengeReq_accepted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.account.user.email


class StateChallenge(models.TextChoices):
    IN_CHALLENGE = ('in_challenge', 'In challenge')
    END_CHALLENGE = ('end_challenge', 'End challenge')


class Challenge(models.Model):
    account_1 = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='challenge_account_1', name='account_1')
    account_2 = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='challenge_account_2', name='account_2')
    wins_account_1 = models.PositiveIntegerField(default=0)
    wins_account_2 = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=15, choices=StateChallenge.choices)
    is_archived = models.BooleanField(default=False)


class ChallengeCategory(models.Model):
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name='ChallengeCategory_CHALENGE')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='ChallengeCategory_CATEGORY')
    created_by = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='ChallengeCategory_accountBy')
    question_1 = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True, null=True, related_name='ChallengeCategory_question_1')
    question_2 = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True, null=True, related_name='ChallengeCategory_question_2')
    question_3 = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True, null=True, related_name='ChallengeCategory_question_3')
    question_4 = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True, null=True, related_name='ChallengeCategory_question_4')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class ChallengeAnswer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='ChallengeAnswer_question')
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='ChallengeAnswer_account')
    challenge_category = models.ForeignKey(
        ChallengeCategory, on_delete=models.CASCADE, related_name='ChallengeAnswer_CHALENGE_CATEGORY')
    answer = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class StateChallengeResult(models.TextChoices):
    WIN_CHALLENGE = ('win', 'Win')
    EQUAL_CHALLENGE = ('equal', 'Equal')
    LOSS_CHALLENGE = ('loss', 'Loss')


class ChallengeResult(models.Model):
    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name='challenge_result_CHALLENGE')
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='challenge_result_account')
    state = models.CharField(
        max_length=5, choices=StateChallengeResult.choices)
    coin = models.IntegerField(default=0)
    xp = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
