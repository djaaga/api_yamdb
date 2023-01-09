from rest_framework import serializers


def validate_username(value):
    """
    Проверка на запрет использования me в качестве username
    """
    if value.lower() == "me":
        raise serializers.ValidationError(
            "Использовать  'me'  username запрещено."
        )
    return value
