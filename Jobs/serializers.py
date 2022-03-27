from rest_framework import serializers
from Jobs.models import Jobs


class JobsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Jobs
        fields = "__all__"
        read_only_fields = ('id', 'created_at')
