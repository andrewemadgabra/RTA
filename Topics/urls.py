from django.urls import path
from Topics.views import MainTopicView, TopicClassificationView, TopicSubcategoriesView


urlpatterns = [
    path('main_topic/', MainTopicView.as_view()),
    path('topic_classification/', TopicClassificationView.as_view()),
    path('topic_subcategories/', TopicSubcategoriesView.as_view()),
]
