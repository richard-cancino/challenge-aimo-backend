from account.models import Note, User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_jwt.serializers import jwt_payload_handler, \
    jwt_encode_handler


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'fullname')
        write_only_fields = ('password',)
        read_only_fields = ('uid',)

    def clean_password(self):
        if len(self.validated_data.get('password')) < 6:
            raise serializers.ValidationError({'details': [{
                'object': 'Error',
                'message': 'Min 6 characters',
            }]})
        else:
            return self.validated_data.get('password')

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            fullname=validated_data.get('fullname')
        )
        password = self.clean_password()
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        error_messages={"blank": "This field is required"})
    password = serializers.CharField(
        error_messages={"blank": "This field is required"})

    def validate(self, attrs):
        self.user_cache = authenticate(email=attrs["email"],
                                       password=attrs["password"])
        if not self.user_cache:
            raise serializers.ValidationError([{
                'object': 'Error',
                'message': "Invalid login",
            }])
        else:
            payload = jwt_payload_handler(self.user_cache)
            return {
                'token': jwt_encode_handler(payload),
                'user': self.user_cache
            }

    def get_user(self):
        return self.user_cache


class CreateNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'description', 'author')


class RetrieveNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'description', 'author', 'is_active',
                  'created_at')
