from rest_framework import serializers
from User.models import User, System, SystemGroup, UserEmploymentJobStatus
from django.contrib.auth.models import (Group, Permission)
from EmploymentStatus.serializers import EmploymentStatusSerializer
from Jobs.serializers import JobsSerializer
from Jobs.models import Jobs
from EmploymentStatus.models import EmploymentStatus
from django.db import transaction


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


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class GroupSerializer(serializers.Serializer):
    system_id = serializers.IntegerField(min_value=0)
    system_name = serializers.CharField(max_length=128)
    id = serializers.IntegerField(min_value=0, read_only=True)
    name = serializers.CharField(max_length=128)
    permissions = serializers.ListField(
        child=serializers.IntegerField(min_value=0, required=True))

    def validate_system_id(self, instance):
        valid_system_id = System.objects.filter(system_id=instance)
        if len(valid_system_id) != 1:
            raise serializers.ValidationError("Not a valid system_id")

        return instance

    def validate_name(self, instance):
        group = Group.objects.filter(name=instance)
        if len(group) > 0:
            raise serializers.ValidationError(
                "group with the same name already exists")
        return instance

    def validate_permissions(self, instance):
        for permission in instance:
            instance_permission = Permission.objects.filter(id=permission)
            if len(instance_permission) != 1:
                raise serializers.ValidationError("Not a valid permission")
        return instance

    @transaction.atomic
    def create(self, validated_data):
        obj = Group.objects.create(name=validated_data['name'])
        obj.permissions.set(validated_data['permissions'])
        obj.save()
        system = System.objects.get(
            system_id=validated_data['system_id'])
        SystemGroup.objects.create(group=obj, system=system)
        return validated_data

    @transaction.atomic
    def update(self, instance, validated_data):
        systemgroup_obj = (SystemGroup.objects.get(group=instance.id))
        if systemgroup_obj.system.system_id != validated_data['system_id']:
            systemgroup_obj.system = System.objects.get(
                system_id=validated_data['system_id'])
            systemgroup_obj.save()

        group_to_save = BaseGroupSerializer(
            instance=instance, data={"name": validated_data['name'],
                                     "permissions": validated_data['permissions']
                                     })
        if group_to_save.is_valid():
            group_to_save.save()
        return validated_data


class UserSerializer(serializers.Serializer):
    CHOICES = (("M", "Male"), ("F", "Female"))
    id = serializers.IntegerField(min_value=0, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    last_login = serializers.DateTimeField(required=False)
    is_superuser = serializers.BooleanField(default=False, write_only=True)
    is_active = serializers.BooleanField(default=True, write_only=True)
    is_staff = serializers.BooleanField(default=False, write_only=True)
    is_admin = serializers.BooleanField(default=False, write_only=True)
    username = serializers.CharField(max_length=30)
    email = serializers.EmailField(max_length=128)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    middle_name = serializers.CharField(max_length=30)
    gender = serializers.MultipleChoiceField(choices=CHOICES)
    number_of_identification = serializers.CharField(max_length=14)
    home_address = serializers.CharField(max_length=45, required=False)
    mobile = serializers.CharField(max_length=14)
    groups = serializers.ListField(
        child=serializers.IntegerField(min_value=0, required=True)
    )
    employment_id = serializers.IntegerField(min_value=0)
    job_id = serializers.IntegerField(min_value=0)

    def validate_employment_id(self, instance):
        if len(EmploymentStatus.objects.filter(employment_id=instance)) != 1:
            raise ValueError('Not a valid employment_id')
        return instance

    def validate_job_id(self, instance):
        if len(Jobs.objects.filter(job_id=instance)) != 1:
            raise ValueError('Not a valid job_id')
        return instance

    def validate(self, attrs):
        return super(UserSerializer, self).validate(attrs)

    @transaction.atomic
    def create(self, validated_data):
        pass
