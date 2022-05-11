from Financial.models import FinancialClaimsStatus
from Financial.serializers import (FinancialClaimsStatusSerializer)

from HelperClasses.GenericView import CRUDView


class FinancialClaimsStatusView(CRUDView):
    base_model = FinancialClaimsStatus
    base_serializer = FinancialClaimsStatusSerializer
