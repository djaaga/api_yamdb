
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from .validator import validate_username


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        return validate_username(value)

    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        model = User


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)
        model = User


class AuthUserSignUpSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        return validate_username(value)

    class Meta:
        fields = (
            "username",
            "email",
        )
        model = User


class AuthUserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, trim_whitespace=True)
    confirmation_code = serializers.CharField(
        required=True, trim_whitespace=True
    )

    def validate(self, attrs):
        data = attrs

        if not User.objects.filter(username=data.get("username")).exists():
            raise exceptions.NotFound("Пользователь не найден.")

        user = User.objects.get(username=data.get("username"))

        if user.confirmation_code != data.get("confirmation_code"):
            raise exceptions.ValidationError("Некорректный код подтверждения.")

        refresh = RefreshToken.for_user(user)

        return {"token": str(refresh.access_token)}

    class Meta:
        fields = (
            "username",
            "confirmation_code",
        )
        model = User
