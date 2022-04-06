from Actors.models import EntityCassification, MainActors, SubActors
from Actors.serializers import (EntityCassificationSerializer, MainActorsGETSerializer,
                                MainActorsSerializer, SubActorsSerializer, SubActorsGETSerializer)
from HelperClasses.GenericView import CRUDView
import os
from django.conf import settings
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

    def handle_static_dir_for_subactor(self, folder_name):
        folder_path = os.path.join(os.path.join(
            settings.BASE_DIR, settings.JSON_CONFIGRATION['STATIC_DIR']), folder_name)
        if not(os.path.isdir(folder_path)):
            os.mkdir(folder_path)

    def get(self, request, pk=None):
        g_model = self.get_model_get
        data, many = self.get_modeled_data(request, pk=pk, model=g_model, field_name=None, field_value=None,
                                           fields_names=[], fields_values=[], debug=False, related_models=['main_actor', "main_actor__entitycassification"], many_to_many_related_models=[])

        return super(SubActorsView, self).get(request, pk, data=data, many=many)

    def post(self, request, modeled_response=False, debug=False, **kwargs):
        folder_name = request.data.get('sub_actor_En')
        self.handle_static_dir_for_subactor(folder_name)
        return super(SubActorsView, self).post(request, modeled_response, debug, **kwargs)

    def put(self, request, pk=None, debug=False, **kwargs):
        folder_name = request.data.get('sub_actor_En')
        self.handle_static_dir_for_subactor(folder_name)
        return super(SubActorsView, self).put(request, pk, debug, **kwargs)

    def patch(self, request, pk=None, debug=False, **kwargs):
        folder_name = request.data.get('sub_actor_En')
        if folder_name is not None:
            self.handle_static_dir_for_subactor(folder_name)

        return super(SubActorsView, self).patch(request, pk, debug, **kwargs)
