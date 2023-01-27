import re

from rest_framework import serializers


def validate_username(value):
    if value.lower() == 'me':
        raise serializers.ValidationError('User not valid')
    if len(value) > 150:
        raise serializers.ValidationError('Not mach len')
    pattern_username = '[A-Za-z0-9+-_@]+'
    if re.match(pattern_username, value) is None:
        raise serializers.ValidationError('Incorrect symbol')
    return value
