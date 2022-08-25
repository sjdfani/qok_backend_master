from django.db import models


class CategoryManager(models.Manager):
    def all(self):
        return self.get_queryset().filter(status=True)


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    status = models.BooleanField(default=False)

    objects = CategoryManager()

    def __str__(self) -> str:
        return self.name
