from Actors.models import EntityCassification, MainActors, SubActors
from Actors.serializers import (EntityCassificationSerializer, MainActorsGETSerializer,
                                MainActorsSerializer, SubActorsSerializer, SubActorsGETSerializer)
from HelperClasses.GenericView import CRUDView

# Create your views here.


class EntityCassificationView(CRUDView):
    base_model = EntityCassification
    base_serializer = EntityCassificationSerializer


class MainActorsView(CRUDView):
    base_model = MainActors
    base_serializer = MainActorsSerializer
    get_serializer = MainActorsGETSerializer

    def get(self, request, pk=None):
        g_model = self.get_model_get
        data = g_model.objects.all().select_related('entitycassification')
        return super(MainActorsView, self).get(request, pk, data=data)


class SubActorsView(CRUDView):
    base_model = SubActors
    base_serializer = SubActorsSerializer
    get_serializer = SubActorsGETSerializer

    def get(self, request, pk=None):
        g_model = self.get_model_get
        data = g_model.objects.all().select_related(
            'main_actor', "main_actor__entitycassification")
        return super(SubActorsView, self).get(request, pk, data=data)
