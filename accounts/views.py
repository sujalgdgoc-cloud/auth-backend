from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()
from .serializers import RegisterUserSerializer, LoginUserSerializer, ProfileUserSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import RegisterUserModel
from rest_framework import generics, status
from rest_framework.response import Response
from .utils import generate_password_reset_token, send_reset_email



class UserRegisterView(generics.CreateAPIView):
    queryset = RegisterUserModel.objects.all()
    serializer_class = RegisterUserSerializer
    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data  = request.data)
        serializers.is_valid(raise_exception = True)
        serializers.save()
        return Response(
            {"msg": "User created successfully"},
            status=status.HTTP_201_CREATED
        )

class UserLoginView(generics.CreateAPIView):
    queryset = RegisterUserModel.objects.all()
    serializer_class = LoginUserSerializer

    def create(self, request, *args, **kargs):
        serializers = self.get_serializer(data = request.data)
        serializers.is_valid(raise_exception = True)
        user = serializers.validated_data["user"] #doubt
        refresh = RefreshToken.for_user(user)
        return Response(
        {"msg": "Login Successfull", 
         "refresh" : str(refresh),
         "access" : str(refresh.access_token)
        },
        status=status.HTTP_200_OK
        )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileUserSerializer(request.user)
        return Response(serializer.data)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        serializer = ChangePasswordSerializer(data = request.data)

        if serializer.is_valid():
            user = request.user

            if not user.check_password(
                serializer.validated_data['old_password']
            ):
                return Response({"msg" : "Old password doesn't match!"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(
                serializer.validated_data['new_password']
            )

            user.save()

            return Response({"msg":"Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors)

class UserResetPasswordView(APIView):

    def post(self, request):
        serializer = ForgotPasswordSerializer(data = request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            user = User.objects.filter(email = email).first()

            if not user:
                return Response({"msg":"User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)

            token = generate_password_reset_token(user)
            send_reset_email(user, token)
            
            return Response(
                {
                    "msg": "Reset email is sent successfully!",
                    "token": token,   # Temporary, just for testing
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data= request.data)

        if serializer.is_valid():

            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            try:
                access_token = AccessToken(token)

                if access_token["type"] != "password-reset":
                    return Response(
                        {"msg": "Invalid token"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user = User.objects.get(id=access_token["user_id"])

                user.set_password(password)
                user.save()

                return Response(
                    {"msg": "Password updated successfully."},
                    status=status.HTTP_200_OK,
                )

            except Exception:
                return Response(
                    {"msg": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )