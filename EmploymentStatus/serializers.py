from rest_framework import serializers
from EmploymentStatus.models import EmploymentStatus


class EmploymentStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmploymentStatus
        fields = "__all__"
        read_only_fields = ('id', 'created_at')
