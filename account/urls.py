from django.urls import path, include
from .views import AccountViewSet, CoinLogViewSet, UpdateAccount, UpdateIconAccount, TotalGames, SummaryCategoryView
from rest_framework import routers


app_name = 'account'


router = routers.SimpleRouter()
router.register('accounts', AccountViewSet, basename='account')
router.register('coin-logs', CoinLogViewSet, basename='coin-log')

urlpatterns = [
    path('summary/', SummaryCategoryView.as_view()),
    path('update-account/', UpdateAccount.as_view()),
    path('update-icon/', UpdateIconAccount.as_view()),
    path('games-count/', TotalGames.as_view()),
    path('', include(router.urls)),
]
