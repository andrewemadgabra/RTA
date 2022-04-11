from Projects.models import Projects, ProjectSections, ProjectContracts
from Projects.serializers import (ProjectsSerializer, ProjectSectionsSerializer,
                                ProjectContractsSerializer, ProjectContractsGETSerializer,
                                ProjectSectionsGETSerializer)

from HelperClasses.GenericView import CRUDView


class ProjectsView(CRUDView):
    base_model = Projects
    base_serializer = ProjectsSerializer


class ProjectSectionsView(CRUDView):
    base_model = ProjectSections
    base_serializer = ProjectSectionsSerializer
    get_serializer = ProjectSectionsGETSerializer


class ProjectContractsView(CRUDView):
    base_model = ProjectContracts
    base_serializer = ProjectContractsSerializer
    get_serializer = ProjectContractsGETSerializer