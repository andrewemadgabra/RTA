from rest_framework import serializers
from Financial.models import FinancialClaimsStatus, FinancialClaims


class FinancialClaimsStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialClaimsStatus
        fields = "__all__"
        read_only_fields = ('financial_claims_status_id', 'created_at')


class FinancialClaimsSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialClaims
        fields = "__all__"
        read_only_fields = ('financial_claims_id', 'created_at')


