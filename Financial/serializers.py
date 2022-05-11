from rest_framework import serializers
from Financial.models import FinancialClaimsStatus


class FinancialClaimsStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialClaimsStatus
        fields = "__all__"
        read_only_fields = ('financial_claims_status_id', 'created_at')
