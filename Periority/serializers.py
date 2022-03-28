from rest_framework import serializers
from Periority.models import DeliveryMethod, AttachmentType, PriorityLevel


class DeliveryMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryMethod
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class AttachmentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttachmentType
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class PriorityLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = PriorityLevel
        fields = "__all__"
        read_only_fields = ('id', 'created_at')
