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
        data, many = self.get_modeled_data(request, pk=pk, model=g_model, field_name=None, field_value=None,
                                           fields_names=[], fields_values=[], debug=False, related_models=['entitycassification'], many_to_many_related_models=[])

        return super(MainActorsView, self).get(request, pk, data=data, many=many)


class SubActorsView(CRUDView):
    base_model = SubActors
    base_serializer = SubActorsSerializer
    get_serializer = SubActorsGETSerializer

    def get(self, request, pk=None):
        g_model = self.get_model_get
        data, many = self.get_modeled_data(request, pk=pk, model=g_model, field_name=None, field_value=None,
                                           fields_names=[], fields_values=[], debug=False, related_models=['main_actor', "main_actor__entitycassification"], many_to_many_related_models=[])

        return super(SubActorsView, self).get(request, pk, data=data, many=many)
