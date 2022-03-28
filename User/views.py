from rest_framework.response import Response
from rest_framework import status
from knox.views import LoginView as KnoxLoginView, LogoutView as KnoxLogoutView
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils import timezone
from django.contrib.auth import get_user_model
from HelperClasses.GenericView import CRUDView, CRUView
from User.models import User, System, SystemGroup,  UserEmploymentJobStatus
from User.serializers import (BaseUserSerializer, BaseGroupSerializer, BaseGroupPermissionSerializer,
                              BasePermissionSerializer, SystemSerializer, SystemGroupGETSerializer,
                              UserEmploymentJobStatusSerializer, SystemGroupSerializer)
from django.contrib.auth.models import (Group, Permission)


# Create your views here.


class UserView(CRUDView):
    base_model = User
    base_serializer = BaseUserSerializer


class UserEmploymentJobStatus(CRUView):
    base_model = UserEmploymentJobStatus
    base_serializer = UserEmploymentJobStatusSerializer


class GroupView(CRUDView):
    base_model = Group
    base_serializer = BaseGroupSerializer
    get_serializer = BaseGroupPermissionSerializer


class SystemGroupView(CRUView):
    base_model = SystemGroup
    base_serializer = SystemGroupSerializer
    get_serializer = SystemGroupGETSerializer


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
