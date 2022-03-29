from rest_framework.response import Response
from rest_framework import status as return_status
from HelperClasses.GenericViewsFolder.BaseView import BaseView


class PutView(BaseView):
    put_model = None
    put_serializer = None

    @property
    def get_model_put(self):
        """
        This property responseble for return put_model for the Service
        if not provided then return base_model
        """
        if self.put_model is None:
            return self.model
        else:
            return self.put_model

    @property
    def get_serializer_put(self):
        """
        This property responseble for return put_serializer for the Service
        if not provided then return base_serializer
        """
        if self.put_serializer is None:
            return self.serializer
        else:
            return self.put_serializer

    def put_json_reseponse_status(self, status):
        return return_status.HTTP_200_OK if status else return_status.HTTP_400_BAD_REQUEST

    def put(self, request, pk=None, debug=False, **kwargs):
        p_model = self.get_model_put
        pk_filed_name = self.pk_field_name_of_model(p_model)
        pk_value = request.data.get(pk_filed_name)
        obj = self.get_model_object_by_pk(pk=pk_value, model=p_model)
        if not(obj):
            object_o, status = {"error": ["Object Not Found"]}, False

        else:
            object_to_save = self.get_serializer_put(instance=obj,
                                                     data=request.data)
            if object_to_save.is_valid():
                object_to_save.save()
                object_o, status = object_to_save.data, True
            else:
                object_o, status = object_to_save.errors, False

        return Response(object_o, status=self.put_json_reseponse_status(status))
