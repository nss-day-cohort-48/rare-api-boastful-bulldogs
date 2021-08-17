from django.db import models
from django.db.models.deletion import CASCADE


class PostTag(models.Model):
    """Create instances of the Tag class"""
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return f'{self.label}'