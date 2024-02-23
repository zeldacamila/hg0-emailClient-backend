from django.db import models
# from django.core.validators import EmailValidator

from user_api.models import User

# Create your models here.


class Email(models.Model):
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
