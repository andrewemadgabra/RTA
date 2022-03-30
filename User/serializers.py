from rest_framework import serializers
from User.models import User, System, SystemGroup, UserEmploymentJobStatus
from django.contrib.auth.models import (Group, Permission)
from django.db import transaction
from Jobs.serializers import JobsSerializer
from EmploymentStatus.serializers import EmploymentStatusSerializer
from Actors.serializers import SubActorsSerializer


class BasePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ('id',)
        extra_kwargs = {
            'content_type': {'write_only': True},
            'codename':  {'write_only': True}
        }


class BaseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions',)
        read_only_fields = ('id',)


class BaseGroupNameONlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')
        read_only_fields = ('id',)


class BaseGroupPermissionSerializer(serializers.ModelSerializer):
    permissions = BasePermissionSerializer(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions',)
        read_only_fields = ('id',)


class BaseUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            password=validated_data['password'],
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name'],
            gender=validated_data['gender'],
            number_of_identification=validated_data['number_of_identification'],
            mobile=validated_data['mobile'],
        )
        user.groups.set(validated_data['groups'])
        user.update_user_permissions()
        return user

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        instance.update_user_permissions()
        return instance


class BaseUserGETSerializer(serializers.ModelSerializer):
    groups = BaseGroupNameONlySerializer(many=True)

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True},
                        'user_permissions': {'write_only':  True}}

    def create(self, validated_data):
        raise ValueError("NOT a vaild Creation Serlizer")


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class SystemGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemGroup
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class SystemGroupGETSerializer(serializers.ModelSerializer):
    system = SystemSerializer()
    group = BaseGroupPermissionSerializer()

    class Meta:
        model = SystemGroup
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class UserEmploymentJobStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserEmploymentJobStatus
        fields = "__all__"
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        user = User.objects.get(id=validated_data['user'])
        user.is_active = True
        user.save()
        return super(UserEmploymentJobStatusSerializer, self).create(validated_data)


class UserEmploymentJobStatusGETSerializer(serializers.ModelSerializer):
    user = BaseUserGETSerializer()
    employment = EmploymentStatusSerializer()
    job = JobsSerializer()
    sub_actor = SubActorsSerializer()

    class Meta:
        model = UserEmploymentJobStatus
        fields = "__all__"
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        raise ValueError("Method not allowed")
