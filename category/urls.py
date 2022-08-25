from django.urls import path, include
from rest_framework import routers
from .views import CategoryViewSet, RandomCategory


app_name = 'category'

router = routers.SimpleRouter()
router.register('', CategoryViewSet, basename='category')

urlpatterns = [
    path('random/', RandomCategory.as_view()),
    path('', include(router.urls)),
]
