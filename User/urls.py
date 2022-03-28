from django.urls import path, include
from User.views import GroupView, PermissionView, Login, Logout, SystemView  # UserView,


urlpatterns = [
    #path('', UserView.as_view()),
    path('system/', SystemView.as_view()),
    path('groups/', GroupView.as_view()),
    path('permission/', PermissionView.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls',
                                    namespace='password_reset')),


]
