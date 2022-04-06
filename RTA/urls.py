"""RTA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("User.urls")),
    path('employemntstatus/', include("EmploymentStatus.urls")),
    path('jobs/', include("Jobs.urls")),
    path('actors/', include("Actors.urls")),
    path('periority/', include("Periority.urls")),
    path('letter/', include("Letter.urls")),
    path('topics/', include("Topics.urls")),
]


urlpatterns += staticfiles_urlpatterns()
