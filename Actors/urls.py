from django.urls import path
from Actors.views import EntityCassificationView, MainActorsView, SubActorsView


urlpatterns = [
    path('entity_classification/', EntityCassificationView.as_view()),
    path('main_actor/', MainActorsView.as_view()),
    path('sub_actor/', SubActorsView.as_view()),
]
