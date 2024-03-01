from django.db import models
from email_api.models.email import Email
from email_api.models.folder import Folder

class FolderEmail(models.Model):

    """
    FolderEmail model 

    Define the FolderEmail model with the following fields:
    - email: The email in the folder foreign key
    - folder: The folder containing the email foreign key

    The model also defines a unique constraint for email and folder.
    The __str__ method returns a string representation of the folder email.
    - {email} in {folder}
    """

    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["email", "folder"]

    def __str__(self):
        return f"{self.email} in {self.folder}"