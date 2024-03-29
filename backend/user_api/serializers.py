from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    This serializer is used to serialize the user model. It is used to return the user data in the response.
    It is also used to validate the user data in the request.

    Fields:
    - id: The user's id.
    - username: The user's username.
    - email: The user's email.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class SignupSerializer(serializers.ModelSerializer):
    """
    This serializer is used to validate the user data in the request when signing up.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class SigninSerializer(serializers.ModelSerializer):
    """
    This serializer is used to validate the user data in the request when signing in.
    """
    username = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(min_length=8, write_only=True, max_length=128, required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

class ValidateTokenSerializer(serializers.Serializer):

    token = serializers.CharField(max_length=255)