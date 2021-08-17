from django.db import models


class Category(models.Model):
    """Create instances of the category class"""
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label
