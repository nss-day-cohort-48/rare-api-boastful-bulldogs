from django.db import models

class Comment(models.Model):
    """Comment model
    fields:
        post (ForeignKey): the post associated with the comment
        author (ForeignKey): the user that made the comment
        content (TextField): text field for comment
        created_on (DateTimeField): the date and time of a comment
    """
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    author = models.ForeignKey("rareUser", on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField()
    