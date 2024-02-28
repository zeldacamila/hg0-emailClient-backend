from django.db import models
from user_api.models import User


class Email(models.Model):
    """
    Email model

    Define the email model with the following fields:
    - subject: The subject of the email
    - body: The body of the email
    - timestamp: The time the email was sent
    - status: The status of the email (read/unread)
    - sender: The user who sent the email
    - recipient: The user who received the email
    - priority: The priority of the email (high/normal/low)

    The model also defines indexes for efficient querying.
    - sender, recipient: For filtering emails by sender and recipient
    - recipient, status: For filtering emails by recipient and status
    - timestamp: For sorting emails by timestamp

    The __str__ method returns a string representation of the email.
    - Email from {sender} to {recipient}: {subject}
    """
    subject = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+")
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+")
    priority = models.CharField(max_length=10, choices=(
        ("high", "High"), ("normal", "Normal"), ("low", "Low")), default="normal")

    # Indexes for efficient querying
    class Meta:
        indexes = [
            models.Index(fields=["sender", "recipient"]),
            models.Index(fields=["recipient", "status"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"Email from {self.sender} to {self.recipient}: {self.subject}"
