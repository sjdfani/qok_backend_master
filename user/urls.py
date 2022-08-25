from django.urls import path
from .views import Register, Verify, Login, RestorePassword, RestorePasswordVerify

app_name = 'user'

urlpatterns = [
    path('register/', Register.as_view()),
    path('verify', Verify.as_view()),
    path('login/', Login.as_view()),
    path('restore-password/', RestorePassword.as_view()),
    path('restore-password/verify/', RestorePasswordVerify.as_view()),
]
