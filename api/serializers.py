from django.contrib.auth.models import Group
from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'middle_name']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        if 'email' in validated_data and validated_data['email'] != instance.email:
            instance.username = validated_data['email']
        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)
    repeat_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'password',
            'repeat_password'
        ]
    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError(
                {"password":"пароли не совпадают"}
            )
        return data
    def create(self, validated_data):
        validated_data.pop('repeat_password')

        user = User(
            username=validated_data['email'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            middle_name = validated_data.get('middle_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()

        user_group = Group.objects.get(name='User')
        user.groups.add(user_group)
        return user
