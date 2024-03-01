from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Folder(models.Model):
    """
    Folder model

    Define the folder model with the following fields:
    - name: The name of the folder
    - user: The user who owns the folder

    The __str__ method returns a string representation of the folder.
    - {name} (Owner: {user})
    """

    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} (Owner: {self.user})"