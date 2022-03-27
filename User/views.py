from lib2to3.pgen2 import token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.user_service import (
    UserService, GroupsService, PermissionsService, SystemService, SystemGroupService, UserEmploymentJobStatusService)
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils import timezone
from django.contrib.auth import get_user_model
from HelperClasses.GenericView import CRUDView


# Create your views here.

class UserView(CRUDView):
    base_service = UserService
    get_service = UserEmploymentJobStatusService

    def post(self, request, *args, **kwargs):
        action_user = request.data.pop('action_user')
        action_user = request.data.pop('job_id')
        ouput, returned_stutus = self.service().post(request, *args, **kwargs)
        if returned_stutus:
            request._full_data = {
                ''
            }


class GroupView(CRUDView):
    base_model = SystemGroupService
    base_service = GroupsService
    get_service = SystemGroupService
    post_service = SystemGroupService
    put_service = SystemGroupService

    def post(self, request, *args, **kwargs):
        system_id = request.data.pop('system_id')
        ouput, returned_stutus = self.service().post(request, *args, **kwargs)
        if returned_stutus:
            group_id = ouput['id']
            request._full_data = {"group": group_id, "system": system_id}
            ouput, returned_stutus = self.get_service_post().post(request, *args, **kwargs)
            if not(returned_stutus):
                request._full_data = {"id": group_id}
                self.service().delete(request, *args, **kwargs)
        returned_stutus = status.HTTP_201_CREATED if returned_stutus else status.HTTP_400_BAD_REQUEST
        return Response(ouput, status=returned_stutus)

    def put(self, request, *args, **kwargs):
        system_id = request.data.pop('system_id')
        id = request.data.get('id')
        ouput, returned_stutus = self.service().put(request, *args, **kwargs)
        if returned_stutus:
            system_group = self.model.objects.filter(
                group=id, system=system_id)
            if len(system_group) > 0:
                system_group = system_group.first().system_group_id
                request._full_data = {
                    "system_group_id": system_group, "group": id, "system": system_id}
                ouput, returned_stutus = self.get_service_put().put(request, *args, **kwargs)
        returned_stutus = status.HTTP_200_OK if returned_stutus else status.HTTP_400_BAD_REQUEST
        return Response(ouput, status=returned_stutus)


class SystemView(CRUDView):
    base_service = SystemService


class PermissionView(CRUDView):
    base_service = PermissionsService


class Login(KnoxLoginView):
    def _get_user_model(self):
        return get_user_model()

    def _delete_user_tokens(self, user):
        AuthToken.objects.filter(
            user=user.id).delete()

    def post(self, request, *args, **kwargs):
        authontication_serializer = AuthTokenSerializer(data=request.data)
        if authontication_serializer.is_valid():
            user = self._get_user_model().objects.get(
                username=request.data['username'])
            old_token = AuthToken.objects.filter(
                user=user.id, expiry__gt=timezone.now())
            if len(old_token) > 0:
                return Response({"error": ["already loged In"]}, status=status.HTTP_400_BAD_REQUEST)
            self._delete_user_tokens(user)
            new_token = super(Login, self).post(request, format=None).data
            return Response(new_token, status=status.HTTP_200_OK)
        return Response(authontication_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(KnoxLogoutView):
    pass
