from django.urls import path
from Financial.views import FinancialClaimsStatusView, FinancialClaimsView


urlpatterns = [
    path('financial_claims_status/', FinancialClaimsStatusView.as_view()),
    path('financial_claims/', FinancialClaimsView.as_view()),
]
