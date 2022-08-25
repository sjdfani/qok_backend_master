from django.urls import path, include
from rest_framework import routers
from .views import CreateQuestion, ReportQuestionView, QuestionByCategory, QuestionWithAcceptState, QuestionWithPendingState, QuestionWithFailedState, RetrieveDeleteQuestion

app_name = 'question'

urlpatterns = [
    path('question-by-category', QuestionByCategory.as_view()),
    path('question-by-accept-state/', QuestionWithAcceptState.as_view()),
    path('question-by-pending-state/', QuestionWithPendingState.as_view()),
    path('question-by-failed-state/', QuestionWithFailedState.as_view()),
    path('create/', CreateQuestion.as_view()),
    path('retrieve-delete/<int:pk>', RetrieveDeleteQuestion.as_view()),
    path('report/', ReportQuestionView.as_view()),
]
