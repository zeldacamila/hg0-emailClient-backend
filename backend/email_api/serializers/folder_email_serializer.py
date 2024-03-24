from rest_framework import serializers

from email_api.models import FolderEmail


class FolderEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderEmail
        fields = "__all__"

    def create(self, validated_data):
        email_data = validated_data.get("email")
        folder_data = validated_data.get("folder")
        if email_data and folder_data:
            folder_email = FolderEmail.objects.create(**validated_data)
            return folder_email
        else:
            raise serializers.ValidationError(
                "Email and folder are required fields")
    
    def update(self, instance, validated_data):
        email_data = validated_data.pop("email")
        folder_data = validated_data.pop("folder")
        if email_data and folder_data:
            email = email_data
            folder = folder_data
            instance.email = email
            instance.folder = folder
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError(
                "Email and folder are required fields")