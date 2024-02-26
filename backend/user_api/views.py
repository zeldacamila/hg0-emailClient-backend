from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import authenticate

from .serializers import SignupSerializer, SigninSerializer, UserSerializer, ValidateTokenSerializer

class AuthViewSet(GenericViewSet):
    """
    AuthViewSet class  for user authentication and authorization operations such as signup, signin and token validation. 
    """
    def get_serializer_class(self):
        """
        Method to return the serializer class based on the action being performed.
        Because the serializer class to be used is dependent on the action being performed, we override the get_serializer_class method 
        to return the appropriate serializer class based on the action being performed.
        """
        if self.action == 'signup':
            return SignupSerializer
        elif self.action == 'signin':
            return SigninSerializer
        else:
            return ValidateTokenSerializer

    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='signup')
    def signup(self, request):
        """
        Method to register a new user.
        Parameters:
        request: The request object with user data to be registered. 
        Returns:
        Response object with the user data and access token if the user is registered successfully, else returns an error message.
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.data['password'])
                user.save()
                user_data = UserSerializer(user).data
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "User registered successfully",
                        "data": {
                             "user": user_data,
                             "access_token": str(refresh.access_token),
                             "refresh_token": str(refresh)
                             },
                        "success": True,
                        "status": status.HTTP_201_CREATED
                    }, 
                    status=status.HTTP_201_CREATED
                    )
        return Response(
                    {
                        "message": serializer.errors,
                        "success": False,
                        "status": status.HTTP_400_BAD_REQUEST
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='signin')
    def signin(self, request):
        """
        Method to authenticate a user.
        Parameters:
        request: The request object with user data to be authenticated. With the user data, the user is authenticated and an access token is generated.
        Returns:
        Response object with the user data and access token if the user is authenticated successfully, else returns an error message.
        """
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                user_data = UserSerializer(user).data
                return Response(
                        {
                            "message": "Signin successful",
                            "data": {
                                "user": user_data,
                                "access_token": str(refresh.access_token),
                                "refresh_token": str(refresh)
                                },
                            "success": True,
                            "status": status.HTTP_200_OK
                        }, 
                        status=status.HTTP_200_OK
                        )
            else:
                return Response(
                    {
                        "message": "Invalid email or password. Please, check the input data and try again.",
                        "success": False,
                        "status": status.HTTP_400_BAD_REQUEST
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(
                    {
                        "message": "Invalid input data. Please, check the input data and try again.",
                        "success": False,
                        "status": status.HTTP_400_BAD_REQUEST
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
    
    @action (detail=False, methods=['post'], permission_classes=[AllowAny])
    def validate_token(self, request):
        """
        Method to validate a token.
        Parameters:
        request: The request object with the token to be validated.
        Returns:
        Response object with a message indicating if the token is valid or not.
        """
        token_serializer = ValidateTokenSerializer(data=request.data)
        if not token_serializer.is_valid():
            return Response(
                {
                    "message": "Token is required",
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST
                }, 
                status=status.HTTP_400_BAD_REQUEST
                )
        try:
            valid_token = AccessToken(token_serializer.data['token'])
            valid_token.check_exp()
            return Response(
                {
                    "message": "Token is valid",
                    "success": True,
                    "status": status.HTTP_200_OK
                }, 
                status=status.HTTP_200_OK
                )
        except TokenError as e:
            return Response(
                {
                    "message": str(e),
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST
                }, 
                status=status.HTTP_400_BAD_REQUEST
                )
