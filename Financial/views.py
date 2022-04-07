from Financial.models import FinancialClaimsStatus, FinancialClaims
from Financial.serializers import (FinancialClaimsStatusSerializer, FinancialClaimsSerializer)

from HelperClasses.GenericView import CRUDView


class FinancialClaimsStatusView(CRUDView):
    base_model = FinancialClaimsStatus
    base_serializer = FinancialClaimsStatusSerializer


class FinancialClaimsView(CRUDView):
    base_model = FinancialClaims
    base_serializer = FinancialClaimsSerializer

