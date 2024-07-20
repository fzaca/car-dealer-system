from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'
