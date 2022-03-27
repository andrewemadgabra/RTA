from rest_framework import serializers
from User.models import User, System, SystemGroup, UserEmploymentJobStatus
from django.contrib.auth.models import (Group, Permission)
from EmploymentStatus.serializers import EmploymentStatusSerializer
from Jobs.serializers import JobsSerializer


class PermissionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ('id',)
        extra_kwargs = {
            'content_type': {'write_only': True},
            'codename':  {'write_only': True}
        }


class GroupBaseSerializer(serializers.ModelSerializer):
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
            is_superuser=validated_data['is_superuser'],
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


class SystemBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class SystemGroupBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemGroup
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class SystemGroupAllFSerializer(serializers.ModelSerializer):
    group = GroupBaseSerializer()
    system = SystemBaseSerializer()

    class Meta:
        model = SystemGroup
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class UserEmploymentJobStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserEmploymentJobStatus
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class UserEmploymentJobStatusAllFSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer()
    employment = EmploymentStatusSerializer()
    job = JobsSerializer()

    class Meta:
        model = UserEmploymentJobStatus
        fields = "__all__"
        read_only_fields = ('id', 'created_at')
