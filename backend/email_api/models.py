from django.db import models
from django.core.validators import EmailValidator

from user_api.models import User

# Create your models here.


class Email(models.Model):
    sender_email = models.EmailField(validators=[EmailValidator()])
    recipient_email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=(
        ("high", "High"), ("normal", "Normal"), ("low", "Low")), default="normal")

    # Indexes for efficient querying
    class Meta:
        indexes = [
            models.Index(fields=["sender_email", "recipient_email"]),
            models.Index(fields=["recipient_email", "status"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"Email from {self.sender_email} to {self.recipient_email}: {self.subject}"
