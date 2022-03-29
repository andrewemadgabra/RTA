from rest_framework.response import Response
from rest_framework import status as return_status
from HelperClasses.GenericViewsFolder.BaseView import BaseView


class PatchView(BaseView):
    patch_model = None
    patch_serializer = None

    @property
    def get_model_patch(self):
        """
        This property responseble for return patch_model for the Service
        if not provided then return base_model
        """
        if self.patch_model is None:
            return self.base_model
        else:
            return self.patch_model

    @property
    def get_serializer_patch(self):
        """
        This property responseble for return patch_serializer for the Service
        if not provided then return base_serializer
        """
        if self.patch_serializer is None:
            return self.base_serializer
        else:
            return self.get_model_patch

    def perpare_data_for_patch(self, request_data, obj, model=None):
        if model is None:
            model = self.patch_model

        fields = list(model._meta.fields)
        new_data = {}
        for field in fields:
            new_data[field.name] = request_data.get(
                field.name, getattr(obj, field.name))
        return new_data

    def patch_json_reseponse_status(self, status):
        return return_status.HTTP_200_OK if status else return_status.HTTP_400_BAD_REQUEST

    def patch(self, request, pk=None, debug=False, **kwargs):
        self.view_validator(request)
        pat_model = self.get_model_patch
        pk_filed_name = self.pk_field_name_of_model(pat_model)
        pk_value = request.data.get(pk_filed_name)
        obj = self.get_model_object_by_pk(pk=pk_value, model=pat_model)
        if not(obj):
            object_o, status = {"error": ["Object Not Found"]}, False

        else:
            pat_serlier = self.get_serializer_patch
            request._full_data = self.perpare_data_for_patch(
                request.data, obj, model=pat_model)
            object_to_save = pat_serlier(instance=obj,
                                         data=request.data)
            if object_to_save.is_valid():
                object_to_save.save()
                object_o, status = object_to_save.data, True
            else:
                object_o, status = object_to_save.errors, False

        return Response(object_o, status=self.patch_json_reseponse_status(status))
