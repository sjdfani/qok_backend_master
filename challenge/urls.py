from django.urls import path
from .views import CreateOrFindMatch, CreateChallengeCategory, CreateChallengeAnswer, OpenChallengeList, EndChallengeList, ChallengeResultView, ChallengeGiveUp


app_name = 'challenge'

urlpatterns = [
    path('match/', CreateOrFindMatch.as_view()),
    path('category/', CreateChallengeCategory.as_view()),
    path('answer/', CreateChallengeAnswer.as_view()),
    path('open-challenge-list/', OpenChallengeList.as_view()),
    path('end-challenge-list/', EndChallengeList.as_view()),
    path('challenge-result/', ChallengeResultView.as_view()),
    path('give-up/', ChallengeGiveUp.as_view()),
]
