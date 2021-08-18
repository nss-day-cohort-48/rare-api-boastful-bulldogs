from django.db import models



class Post(models.Model):
    """Post Model
    """
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    content = models.TextField()
    approved = models.BooleanField()
    image_url = models.TextField()
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="tags")
