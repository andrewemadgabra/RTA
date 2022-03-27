from django.urls import path
from Jobs.views import JobsView


urlpatterns = [
    path('', JobsView.as_view()),
]
