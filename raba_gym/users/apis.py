from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from django.core.validators import MinLengthValidator
from .validators import number_validator, special_char_validator, letter_validator
from raba_gym.users.models import User , Profile
from raba_gym.api.mixins import ApiAuthMixin
from raba_gym.users.selectors import get_profile
from raba_gym.users.services import register 
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from drf_spectacular.utils import extend_schema


class ProfileApi(ApiAuthMixin, APIView):

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile 
            fields = ("bio",)

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        query = get_profile(user=request.user)
        return Response(self.OutputSerializer(query, context={"request":request}).data)


class RegisterApi(APIView):

    class InputRegisterSerializer(serializers.Serializer):
        phone = serializers.CharField(
            max_length=11,
            required=True,
            error_messages={
                "blank": "موبایل خود را وارد نمایید",
                "required": "موبایل خود را وارد نمایید",
            },
        )
        bio = serializers.CharField(max_length=1000, required=False)
        
        def validate_phone(self, phone):
            if User.objects.filter(phone=phone).exists():
                raise serializers.ValidationError("کاربری با این موبایل وجود دارد", code="authorization")
            
            return phone
        
        def validate(self, attrs):
            phone = attrs.get("phone")
            if not phone.isdigit():
                return super().validate(attrs)
            return attrs

    class OutputRegisterSerializer(serializers.ModelSerializer):

        token = serializers.SerializerMethodField("get_token")

        class Meta:
            model = User 
            fields = ("phone", "token", "created_at", "updated_at")

        def get_token(self, user):
            pass
    #         data = dict()
    #         token_class = RefreshToken

    #         refresh = token_class.for_user(user)

    #         data["refresh"] = str(refresh)
    #         data["access"] = str(refresh.access_token)

    #         return data


    @extend_schema(request=InputRegisterSerializer, responses=OutputRegisterSerializer)
    def post(self, request):
        serializer = self.InputRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = register(
                    phone=serializer.validated_data.get("phone"),
                    bio=serializer.validated_data.get("bio")
                    )
        except Exception as ex:
            return Response(
                    f"Database Error {ex}",
                    status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(self.OutputRegisterSerializer(user, context={"request":request}).data)

