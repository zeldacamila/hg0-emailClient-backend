from django.db import models

from user_api.models import User

# Create your models here.


class Email(models.Model):
    sender_email = models.EmailField()
    recipient_email = models.EmailField()
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
