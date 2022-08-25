from django.contrib import admin
from .models import Challenge, ChallengeAnswer, ChallengeCategory, ChallengeRequest, ChallengeResult


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('account_1', 'account_2', 'created', 'ended', 'state')
    list_filter = ('state',)


@admin.register(ChallengeCategory)
class ChallengeCategoryAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'category', 'created_by', 'created_at')
    list_filter = ('category',)


@admin.register(ChallengeAnswer)
class ChallengeAnswerAdmin(admin.ModelAdmin):
    list_display = ('account', 'challenge_category', 'created_at')


@admin.register(ChallengeRequest)
class ChallengeRequestAdmin(admin.ModelAdmin):
    list_display = ('account', 'accepted_by', 'created_at', 'accepted_at')
    list_filter = ('account',)


@admin.register(ChallengeResult)
class ChallengeResultAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'account',
                    'created_at', 'state', 'coin', 'xp')
    list_filter = ('account', 'challenge', 'state')
