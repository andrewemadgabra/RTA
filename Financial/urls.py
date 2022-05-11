from django.urls import path
from Financial.views import FinancialClaimsStatusView


urlpatterns = [
    path('financial_claims_status/', FinancialClaimsStatusView.as_view()),
]
