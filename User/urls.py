from django.urls import path, include
from User.views import (GroupView, PermissionView, Login, ForceLogin, Logout, SystemView,
                        UserView, UserEmploymentJobStatus, SystemGroupView)


urlpatterns = [
    path('', UserView.as_view()),
    path('user_assign_job/', UserEmploymentJobStatus.as_view()),
    path('system/', SystemView.as_view()),
    path('groups/', GroupView.as_view()),
    path('groups_system/', SystemGroupView.as_view()),
    path('permission/', PermissionView.as_view()),
    path('login/', Login.as_view()),
    path('force_login/', ForceLogin.as_view()),
    path('logout/', Logout.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls',
                                    namespace='password_reset')),


]
