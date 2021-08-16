from django.db import models


class Post(models.Model):
    """Event Model
    Fields:
        user_id (ForeignKey): the user that made the event
        category_id (ForeignKey): the game associated with the event
        date (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (TextField): The text description of the event
        title (CharField): The title of the event
        attendees (ManyToManyField): The gamers attending the event
    """
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    time = models.TimeField()
    content = models.TextField()
    approved = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.post.title} on {self.publication_date} hosted by {self.user_id.name}'
    
    @property
    def joined(self):
        return self.__joined

    @joined.setter
    def joined(self, value):
        self.__joined = value

    @property
    def user_name(self):
        name = self.user_id.name()
        return name