from django.db import models
from user.models import CustomUser


class AccountIcon(models.Model):
    icon = models.ImageField(upload_to='icons/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Icon'


class Account(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, name='user')
    coin = models.IntegerField()
    icon = models.ForeignKey(
        AccountIcon, on_delete=models.CASCADE, null=True, blank=True, name='icon')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email


class Level(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE)
    stage = models.PositiveIntegerField(default=1)
    minimum = models.PositiveIntegerField(default=0)
    maximum = models.PositiveIntegerField(default=10)

    def __str__(self) -> str:
        return self.account.user.email


class CoinLog(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, name='account')
    amount = models.IntegerField()
    description = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.account.user.email
