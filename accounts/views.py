from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.state import token_backend
from .models import User
from .validators import validate_user_data
from .serializers import UserSerializer, UserProfileSerializer

# Create your views here.
class UserCreateView(APIView):# send_verification_eamil
    permission_classes = [AllowAny]

    def post(self, request):
        rlt_message = validate_user_data(request.data)
        if len(rlt_message) > 0:
            return Response({"message": rlt_message}, status=400)


        user = User.objects.create_user(
            username = request.data.get("username"),
            email = request.data.get("email"),
            password =request.data.get("password"),
            nickname = request.data.get("nickname"),
            birthday = request.data.get("birthday"),
            gender = request.data.get("gender"),
            introduction = request.data.get("introduction"),
        )
        # user = User.objects.create_user(**request)

        refresh = RefreshToken.for_user(user) # 토큰 발급

        serializer = UserSerializer(user)
        response_dict = serializer.data
        response_dict["access"] = str(refresh.access_token)
        response_dict["refresh"] = str(refresh)
        return Response(response_dict) 


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")


        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"message": "username과 Password가 일차하지 않거나 존재하지 않습니다."}, 
                status=400,
            )


        refresh = RefreshToken.for_user(user)
        return Response(
        {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    )


class UserProfileView(APIView):

    def get(self, request, username):
        user = User.objects.get(username=username)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class UserLogoutView(APIView):


    def post(self, request, *args, **kwargs):
        try:
            # 사용자로부터 받은 토큰을 무효화합니다.
            refresh_token = request.data.get('refresh_token')
            print(refresh_token, request.data)
            if not refresh_token:
                return Response(
                    {'detail': 'Refresh token is required.'}, 
                    status=400
                    )
            
            # RefreshToken 인스턴스를 생성하여 Blacklist에 추가합니다.
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'detail': 'Logged out successfully.'}, 
                status=400
                )
        except TokenError:
            return Response(
                {'detail': 'Token is invalid or expired.'}, 
                status=400
                )