from rest_framework.response import Response
from rest_framework import status
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils import timezone
from django.contrib.auth import get_user_model
from HelperClasses.GenericView import CRUDView
from User.models import User, System, SystemGroup,  UserEmploymentJobStatus
from User.serializers import (BaseUserSerializer, GroupSerializer,
                              BasePermissionSerializer, SystemSerializer)
from django.contrib.auth.models import (Group, Permission)
from django.db.models import F as model_function


# Create your views here.

# class UserView(CRUDView):
#     base_model = UserEmploymentJobStatus
#     base_service = UserService
#     get_service = UserEmploymentJobStatusService
#     post_service = UserEmploymentJobStatusService
#     put_service = UserEmploymentJobStatusService

#     def post(self, request, *args, **kwargs):
#         action_user = request.data.pop('action_user')
#         job_id = request.data.pop('job_id')
#         employment_id = request.data.pop('employment_id')

#         output, returned_stutus = self.service().post(request, *args, **kwargs)
#         if returned_stutus:
#             user_id = output['id']
#             request._full_data = {
#                 'action_user':  action_user,
#                 'job': job_id,
#                 'employment': employment_id,
#                 'user': user_id
#             }
#             output, returned_stutus = self.get_service_post().post(request, *args, **kwargs)
#             if not(returned_stutus):
#                 request._full_data = {
#                     'id': user_id
#                 }
#                 self.service().delete(request, *args, **kwargs)
#         returned_stutus = status.HTTP_201_CREATED if returned_stutus else status.HTTP_400_BAD_REQUEST
#         return Response(output, status=returned_stutus)

#     def put(self, request, *args, **kwargs):
#         action_user = request.data.pop('action_user')
#         job_id = request.data.pop('job_id')
#         employment_id = request.data.pop('employment_id')
#         id = request.data.get('id')
#         output, returned_stutus = self.service().put(request, *args, **kwargs)
#         if returned_stutus:
#             user_job_emp = self.model.objects.filter(
#                 user=id)
#             if len(user_job_emp) > 0:
#                 user_job_emp = user_job_emp.first().user_employment_id
#                 request._full_data = {
#                     'user_employment_id': user_job_emp,
#                     'action_user':  action_user,
#                     'job': job_id,
#                     'employment': employment_id,
#                     'user': id
#                 }
#                 output, returned_stutus = self.get_service_put().put(
#                     request, *args, **kwargs)

#         returned_stutus = status.HTTP_200_OK if returned_stutus else status.HTTP_400_BAD_REQUEST
#         return Response(output, status=returned_stutus)


class GroupView(CRUDView):
    base_model = Group
    base_serializer = GroupSerializer
    get_model = SystemGroup

    def get(self, request, pk=None):
        g_model = self.get_model_get
        b_model = self.model
        g_serializer = self.get_serializer_get
        groups_systems = (g_model.objects.all().prefetch_related(
            'group', 'system')
            .values('group__id', 'group__name', 'system__system_id', 'system__system_ar'))
        data_to_serializer = []
        for group_system in groups_systems:
            data_to_serializer.append(
                {
                    "system_id": group_system['system__system_id'],
                    "system_name":  group_system['system__system_ar'],
                    "id": group_system['group__id'],
                    "name": group_system['group__name'],
                    "permissions": [permission['id'] for permission in b_model.objects.get(
                        id=group_system['group__id']).permissions.all().values('id')]
                }
            )
        serlized_data = g_serializer(data_to_serializer, many=True)
        return Response(serlized_data.data, status=status.HTTP_200_OK)


class SystemView(CRUDView):
    base_model = System
    base_serializer = SystemSerializer


class PermissionView(CRUDView):
    base_model = Permission
    base_serializer = BasePermissionSerializer

    def __handel_missing_data_in_permssion(self, request):
        name = request.data.get('name')
        request.data['codename'] = name
        request.data['content_type'] = 1
        return request

    def post(self, request, *args, **kwargs):
        request = self.__handel_missing_data_in_permssion(request)
        return super(PermissionView, self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        request = self.__handel_missing_data_in_permssion(request)
        return super(PermissionView, self).put(request, *args, **kwargs)


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
