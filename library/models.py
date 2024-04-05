from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField(blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    # Add a foreign key to link the book to the user who owns it
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    