from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, SigninSerializer

class AuthViewSet(ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='signup')
    def signup(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.data['password'])
                user.save()
                user_data = SigninSerializer(user).data
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
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            user_data = SigninSerializer(user).data
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
        return Response(
                    {
                        "message": "Invalid email or password. Please, check the input data and try again.",
                        "success": False,
                        "status": status.HTTP_400_BAD_REQUEST
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                    )
    @action (detail=False, methods=['post'], permission_classes=[AllowAny])
    def validate_token(self, request):
        token = request.data.get('token')
        if not token:
            return Response(
                {
                    "message": "Token is required",
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST
                }, 
                status=status.HTTP_400_BAD_REQUEST
                )
        try:
            valid_token = AccessToken(token)
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
