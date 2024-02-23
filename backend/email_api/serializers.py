from rest_framework import serializers
from email_api.models import Email
from user_api.models import User
from django.core.exceptions import ObjectDoesNotExist


class EmailSerializer(serializers.ModelSerializer):
    sender_email = serializers.EmailField(write_only=True)
    recipient_email = serializers.EmailField(write_only=True)

    class Meta:
        model = Email
        fields = ["sender_email",
                  "recipient_email",
                  "subject",
                  "body",
                  "timestamp",
                  "status",
                  "priority",]
        read_only_fields = ["timestamp",]

    def create(self, validated_data):
        sender_email = validated_data.pop("sender_email")
        recipient_email = validated_data.pop("recipient_email")

        sender = self.get_user_by_email(sender_email, "Sender")
        recipient = self.get_user_by_email(recipient_email, "Recipient")

        email = Email.objects.create(
            sender=sender, recipient=recipient, **validated_data)

        return email

    def get_user_by_email(self, email, user_type):
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                f"{user_type} with email '{email}' does not exist")
