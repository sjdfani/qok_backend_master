from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create(self, email, password, **kwargs):
        if email is None:
            raise ValueError("email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create(email, password, **kwargs)
