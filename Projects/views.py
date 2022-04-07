from Projects.models import Projects, ProjectSections, ProjectContracts
from Projects.serializers import (ProjectsSerializer, ProjectSectionsSerializer,
                                ProjectContractsSerializer)

from HelperClasses.GenericView import CRUDView


class ProjectsView(CRUDView):
    base_model = Projects
    base_serializer = ProjectsSerializer


class ProjectSectionsView(CRUDView):
    base_model = ProjectSections
    base_serializer = ProjectSectionsSerializer


class ProjectContractsView(CRUDView):
    base_model = ProjectContracts
    base_serializer = ProjectContractsSerializer
