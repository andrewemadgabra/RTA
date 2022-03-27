from EmploymentStatus.employment_service import EmploymentStatusService
from HelperClasses.GenericView import CRUDView

# CreaEmploymentStatuste your views here.


class EmploymentStatusView(CRUDView):
    base_service = EmploymentStatusService