from django.contrib import admin
from .models import Account, CoinLog, Level, AccountIcon


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin', 'created')


@admin.register(CoinLog)
class CoinLogAdmin(admin.ModelAdmin):
    list_display = ('account', 'amount', 'created')
    list_filter = ('account',)


@admin.register(Level)
class CoinLogAdmin(admin.ModelAdmin):
    list_display = ('account', 'stage', 'minimum', 'maximum')
    list_filter = ('account',)


@admin.register(AccountIcon)
class AccountIconsAdmin(admin.ModelAdmin):
    list_display = ('uploaded_at',)
