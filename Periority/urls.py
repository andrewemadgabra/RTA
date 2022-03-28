from django.urls import path
from Periority.views import DeliveryMethodView, AttachmentTypeView, PriorityLevelView


urlpatterns = [
    path('delivery_method/', DeliveryMethodView.as_view()),
    path('attachment_type/', AttachmentTypeView.as_view()),
    path('priority_level/', PriorityLevelView.as_view()),
]
