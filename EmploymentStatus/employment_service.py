from EmploymentStatus.models import EmploymentStatus
from EmploymentStatus.serializers import EmploymentStatusSerializer
from HelperClasses.GenericService import CRUDService


class EmploymentStatusService(CRUDService):
    base_model = EmploymentStatus
    base_serializer = EmploymentStatusSerializer
