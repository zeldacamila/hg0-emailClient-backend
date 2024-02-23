from rest_framework import serializers
from email_api.models import Email


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ["sender",
                  "recipient",
                  "subject",
                  "body",
                  "timestamp",
                  "status",
                  "priority",]
        read_only_fields = ["timestamp"]
