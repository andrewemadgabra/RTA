from EmploymentStatus.models import EmploymentStatus
from EmploymentStatus.serializers import EmploymentStatusSerializer
from HelperClasses.GenericView import CRUDView

# CreaEmploymentStatuste your views here.


class EmploymentStatusView(CRUDView):
    base_model = EmploymentStatus
    base_serializer = EmploymentStatusSerializer
