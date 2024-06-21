from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            User = get_user_model()
            try:
                user = User.objects.get(username=username)
                # Utilisez check_password pour comparer le mot de passe en texte brut au hachage stocké
                if not check_password(password, user.password):
                    raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
            except User.DoesNotExist:
                raise serializers.ValidationError('Unable to log in with provided credentials.', code='authorization')
        else:
            raise serializers.ValidationError('Must include "username" and "password".', code='authorization')

        attrs['user'] = user
        return attrs