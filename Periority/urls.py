from django.urls import path
from Periority.views import DeliveryMethodView, PriorityLevelView


urlpatterns = [
    path('delivery_method/', DeliveryMethodView.as_view()),
    path('priority_level/', PriorityLevelView.as_view()),
]
