from Topics.models import MainTopic, TopicClassification, TopicSubcategories
from Topics.serializers import (MainTopicSerializer, TopicClassificationSerializer,
                                TopicSubcategoriesSerializer, TopicClassificationGETSerializer,
                                TopicSubcategoriesGETSerializer)

from HelperClasses.GenericView import CRUDView


class MainTopicView(CRUDView):
    base_model = MainTopic
    base_serializer = MainTopicSerializer


class TopicClassificationView(CRUDView):
    base_model = TopicClassification
    base_serializer = TopicClassificationSerializer
    get_serializer = TopicClassificationGETSerializer


class TopicSubcategoriesView(CRUDView):
    base_model = TopicSubcategories
    base_serializer = TopicSubcategoriesSerializer
    get_serializer = TopicSubcategoriesGETSerializer
