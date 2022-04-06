from rest_framework import serializers
from Topics.models import MainTopic, TopicClassification, TopicSubcategories


class MainTopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainTopic
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class TopicClassificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicClassification
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class TopicSubcategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopicSubcategories
        fields = "__all__"
        read_only_fields = ('id', 'created_at')
