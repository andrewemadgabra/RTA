from django.urls import path
from EmploymentStatus.views import EmploymentStatusView


urlpatterns = [
    path('', EmploymentStatusView.as_view()),
]
