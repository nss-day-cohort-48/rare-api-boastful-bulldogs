from django.db import models


class Tag(models.Model):
    """Create instances of the Tag class"""
    label = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.label}'