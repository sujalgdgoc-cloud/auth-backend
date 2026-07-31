from rest_framework import serializers

from .models import RegisterUserModel
from rest_framework.response import Response
from rest_framework.authentication import authenticate
class RegisterUserSerializer(serializers.ModelSerializer): #model serializer wha use krna zaha new user create ho rha ho
    password = serializers.CharField(max_length=255, style = {'input_type': 'password'}, write_only = True)
    password2 = serializers.CharField(max_length=255, style = {'input_type': 'password'}, write_only = True)
    def validate(self, data):
        password = data.get('password')
        password2 = data.get("password2")
        if(password != password2):
            raise serializers.ValidationError('password and confirm password should match')

        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        password = validated_data.pop('password')

        user = RegisterUserModel(**validated_data)

        user.set_password(password)#waha pr password hash krhe hai

        user.save()
        
        return user
    
    class Meta:
        model = RegisterUserModel
        fields = ['email', 'name', 'password', 'password2']

class LoginUserSerializer(serializers.Serializer):
    #model serializer is not required in Login fields as no new user is created
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(
            username = email,
            password = password
        )

        if user is None:
            raise serializers.ValidationError('Enter vaild email and password')

        data['user'] = user
        return data

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserModel
        fields = ['id','name', 'email']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only = True)
    new_password = serializers.CharField(write_only = True)

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only = True)
    