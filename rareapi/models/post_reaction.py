from django.db import models
from django.db.models.deletion import CASCADE


class PostReaction(models.Model):
    """Create instances of the Tag class"""
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return f'{self.label}'