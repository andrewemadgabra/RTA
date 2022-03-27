from User.models import User, System, SystemGroup,  UserEmploymentJobStatus
from User.serializers import (BaseUserSerializer, GroupBaseSerializer,
                              PermissionBaseSerializer, SystemBaseSerializer,
                              SystemGroupBaseSerializer, SystemGroupAllFSerializer,
                              UserEmploymentJobStatusSerializer, UserEmploymentJobStatusAllFSerializer)
from django.contrib.auth.models import (Group, Permission)
from HelperClasses.GenericService import CRUDService


class GroupsService(CRUDService):
    base_model = Group
    base_serializer = GroupBaseSerializer


class SystemService(CRUDService):
    base_model = System
    base_serializer = SystemBaseSerializer


class SystemGroupService(CRUDService):
    base_model = SystemGroup
    base_serializer = SystemGroupBaseSerializer
    get_serializer = SystemGroupAllFSerializer

    def __get_permissions_serlized(self, groups, groupsSerilzed):
        for index, group in enumerate(groups):
            groupsSerilzed[index]['group'].pop('permissions')
            groupsSerilzed[index]['group']['permissions'] = (PermissionBaseSerializer(
                group.group.permissions.all(), many=True).data)

        return groupsSerilzed

    def get(self, request, *args, **kwargs):
        permissions_obj = request.GET.get('permissions_obj')
        groups = super(SystemGroupService, self).get_modeled_data(
            request, *args, **kwargs)
        groupsSerilzed = super(SystemGroupService, self).get(
            request, data=groups, *args, **kwargs)
        if permissions_obj:
            groups = self.__get_permissions_serlized(groups, groupsSerilzed)
        return groupsSerilzed


class PermissionsService(CRUDService):
    base_model = Permission
    base_serializer = PermissionBaseSerializer

    def __handel_missing_data_in_permssion(self, request):
        name = request.data.get('name')
        request.data['codename'] = name
        request.data['content_type'] = 1
        return request

    def post(self, request, *args, **kwargs):
        request = self.__handel_missing_data_in_permssion(request)
        return super(PermissionsService, self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        request = self.__handel_missing_data_in_permssion(request)
        return super(PermissionsService, self).put(request, *args, **kwargs)


class UserService(CRUDService):
    base_model = User
    base_serializer = BaseUserSerializer

    def __get_permissions_serlized(self, users, usersSerlizer):
        for index, user in enumerate(users):
            usersSerlizer[index].pop('user_permissions')
            usersSerlizer[index]['user_permissions'] = (PermissionBaseSerializer(
                user.user_permissions.all(), many=True).data)

        return users

    def __get_groups_serlized(self, users, usersSerlizer):
        for index, user in enumerate(users):
            usersSerlizer[index].pop('groups')
            usersSerlizer[index]['groups'] = (GroupBaseSerializer(
                user.groups.all(), many=True).data)
        return usersSerlizer

    def __get_groups_permissions_serlized(self, users, usersSerlizer):
        for index, user in enumerate(users):
            usersSerlizer[index].pop('groups')
            usersSerlizer[index]['groups'] = (GroupBaseSerializer(
                user.groups.all(), many=True).data)
            usersSerlizer[index].pop('user_permissions')
            usersSerlizer[index]['user_permissions'] = (PermissionBaseSerializer(
                user.user_permissions.all(), many=True).data)
        return usersSerlizer

    def get(self, request, *args, **kwargs):
        get_group = request.GET.get('get_group')
        get_permissions = request.GET.get('get_permissions')
        users = super(UserService, self).get_modeled_data(
            request, *args, **kwargs)
        usersSerlizer = super(UserService, self).get(
            request, data=users, *args, **kwargs)
        if get_group and get_permissions:
            usersSerlizer = self.__get_groups_permissions_serlized(
                users, usersSerlizer)
        elif get_group and not(get_permissions):
            usersSerlizer = self.__get_groups_serlized(users, usersSerlizer)
        elif get_permissions and not(get_group):
            usersSerlizer = self.__get_permissions_serlized(
                users, usersSerlizer)
        return usersSerlizer


class UserEmploymentJobStatusService(CRUDService):
    base_model = User
    base_serializer = BaseUserSerializer
    get_serializer = UserEmploymentJobStatusAllFSerializer
    get_model = UserEmploymentJobStatus
    post_serializer = UserEmploymentJobStatusSerializer
    put_model = UserEmploymentJobStatus
    put_serializer = UserEmploymentJobStatusSerializer

    def get(self, request, *args, **kwargs):
        data = self.get_model_get.objects.all().select_related(
            'user',  'employment', 'job')
        return super(UserEmploymentJobStatusService, self).get(request, data=data, *args, **kwargs)
