from django.urls import path
from Projects.views import ProjectsView, ProjectSectionsView, ProjectContractsView


urlpatterns = [
    path('projects/', ProjectsView.as_view()),
    path('project_sections', ProjectSectionsView.as_view()),
    path('project_contracts/', ProjectContractsView.as_view()),
]
