from django.contrib import admin
from .models import Question, ReportQuestion


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'created', 'updated', 'state')
    list_filter = ('user', 'category', 'state')


@admin.register(ReportQuestion)
class ReportQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'report')
    list_filter = ('question', 'report')
