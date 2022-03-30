from rest_framework import serializers
from Letter.models import LetterData, AttachmentType


class LetterDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = LetterData
        fields = '__all__'
        read_only_fields = ('letter_data_id', 'created_at')


class AttachmentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttachmentType
        fields = "__all__"
        read_only_fields = ('id', 'created_at')
