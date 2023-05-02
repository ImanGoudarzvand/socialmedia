from django.shortcuts import render
from django.core.validators import MinLengthValidator
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from socialmedia.users.models import User, Profile
from socialmedia.api.mixins import ApiAuthMixin
from .validators import number_validator, letter_validator, special_char_validator
from socialmedia.users.services.user import register
from socialmedia.users.selectors.profile import get_profile
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterApi(APIView):


    class InputRegisterSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=255)
        password = serializers.CharField(validators=[
                                    number_validator,
                                    letter_validator,
                                    special_char_validator,
                                    MinLengthValidator(limit_value=10)
                                                    ])
        bio = serializers.CharField(max_length=500, required = False)

        confirm_password = serializers.CharField(max_length=255)

        def validate_username(self, username):
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError("username already taken")

            return username

        def validate(self, data):
            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("password and confirm password shoud be the same!")

            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("password or confirm password required!")

            return data


    class OutputRegisterSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('username', 'created_at', 'updated_at')

    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request):
        
        serializer = self.InputRegisterSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = register(username=serializer.validated_data.get('username'),
                            password=serializer.validated_data.get('password'),
                            bio=serializer.validated_data.get('bio'))
        except Exception as err:
            return Response(data = f"Database Error {err}", status=status.HTTP_400_BAD_REQUEST)

        response_message = self.OutputRegisterSerializer(user).data
        refresh = RefreshToken.for_user(user)
        response_message["access"] = str(refresh.access_token)
        response_message["refresh"] = str(refresh)

        return Response(response_message , status=status.HTTP_201_CREATED)

class ProfileApi(ApiAuthMixin,APIView):

    class OutputProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('bio', 'subscribers_count', 'subscriptions_count', 'posts_count')

    @extend_schema(responses=OutputProfileSerializer)
    def get(self, request):
        queryset = get_profile(user=request.user)

        return Response(self.OutputProfileSerializer(queryset).data, status=status.HTTP_200_OK)