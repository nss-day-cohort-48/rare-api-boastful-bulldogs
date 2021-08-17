from django.db import models
# from rareapi.models.tag import Tag
from django.contrib.auth.models import User


class Post(models.Model):
    """Post Model
    """
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    time = models.TimeField()
    content = models.TextField()
    approved = models.BooleanField()
    tags = models.ManyToManyField("Tag", through="PostTag", related_name="tags")

    # def __str__(self) -> str:
    #     return f'{self.title} on {self.publication_date} hosted by {self.user_id.name}'

    # @property
    # def joined(self):
    #     return self.__joined

    # @joined.setter
    # def joined(self, value):
    #     self.__joined = value

    # # @property
    # # def user_name(self):
    # #     name = self.user_id.name()
    # #     return name