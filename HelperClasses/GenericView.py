from turtle import mode
from importlib_metadata import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as return_status


class BaseView(APIView):
    base_model = None
    base_serializer = None

    @property
    def model(self):
        """
        This property responseble for return base_model for the Service
        """
        if self.base_model is None:
            raise TypeError('base_model was not provided')
        else:
            return self.base_model

    @property
    def serializer(self):
        """
        This property responseble for return base_serializer for the Service
        """
        if self.base_serializer is None:
            raise TypeError('base_serializer was not provided')
        else:
            return self.base_serializer

    def view_validator(self, request):
        return None

    def get_model_object_by_pk(self, pk, model=None):
        """
        This function is responseble for get one element of the model 
        input : pk -> key value search
                model -> optional, if not provided then base_model will be used 
        ouput object from model or None if not existed 
        """
        if model is None:
            model = self.model
        try:
            obj = model.objects.get(pk=pk)
            return obj
        except model.DoesNotExist:
            return

    def pk_field_name_of_model(self, model):
        if not(model):
            model = self.base_model
        return model._meta.pk.name


class GetView(BaseView):
    get_model = None
    get_serializer = None

    @property
    def get_model_get(self):
        """
        This property responseble for return get_model for the Service
        if not provided then return base_model
        """
        if self.get_model is None:
            return self.model
        else:
            return self.get_model

    @property
    def get_serializer_get(self):
        """
        This property responseble for return get_serializer for the Service
        if not provided then return base_serializer
        """
        if self.get_serializer is None:
            return self.serializer
        else:
            return self.get_serializer

    def get_modeled_data(self, request, pk=None, model=None, filed_name=None, field_value=None,
                         fields_names=[], fields_values=[], debug=False):
        """
        This function is responseble for getting data from the model itself
        """
        if model is None:
            model = self.get_model_get

        return model.objects.all()

    def get_serialized_data(self, request, model=None, data=None, pk=None, filed_name=None, field_value=None,
                            fields_names=[], fields_values=[], debug=False):
        """
        This function is responseble for getting serialized data 
        input : data -> optional, if not provided then use get_modeled_data from self. 
                        if provided then this data will be used to be serialized
        """
        if model is None:
            model = self.model
        if not(data):
            data = self.get_modeled_data(
                request=request, pk=pk, model=model, filed_name=filed_name, field_value=field_value,
                fields_names=fields_names, fields_values=fields_values, debug=debug)
        return self.get_serializer_get(data, many=True).data

    def get(self, request, pk=None, modeled_response=False,
            debug=False, **kwargs):
        data = self.get_modeled_data(request, pk=pk, debug=debug)
        serlized_data = self.get_serialized_data(
            request, data=data, pk=pk, debug=debug)
        return Response(serlized_data, status=return_status.HTTP_200_OK)


class PostView(BaseView):
    post_model = None
    post_serializer = None

    @property
    def get_model_post(self):
        """
        This property responseble for return post_model for the Service
        if not provided then return base_model
        """
        if self.post_model is None:
            return self.model
        else:
            return self.post_model

    @property
    def get_serializer_post(self):
        """
        This property responseble for return post_serializer for the Service
        if not provided then return base_serializer
        """
        if self.post_serializer is None:
            return self.serializer
        else:
            return self.post_serializer

    def post_json_reseponse_status(self, status):
        return return_status.HTTP_201_CREATED if status else return_status.HTTP_400_BAD_REQUEST

    def post(self, request, modeled_response=False, debug=False, **kwargs):
        """
        This function is reseponseble for create new object from the model given.
        The model can be get_model_post if not existed  then use base_model.

        This function return seralized data or error , and status (bool) to identifiy whethere it successfully created 
        or not.
        """
        self.view_validator(request)
        object_to_save = self.get_serializer_post(
            data=request.data)
        if object_to_save.is_valid():
            object_to_save.save()
            object_o, status = object_to_save.data, True
        else:
            object_o, status = object_to_save.errors, False

        return Response(object_o, status=self.post_json_reseponse_status(status))


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


class DeleteView(BaseView):
    delete_model = None
    delete_serializer = None

    @property
    def get_model_delete(self):
        """
        This property responseble for return delete_model for the Service
        if not provided then return base_model
        """
        if self.delete_model is None:
            return self.base_model
        else:
            return self.delete_model

    @property
    def get_serializer_delete(self):
        """
        This property responseble for return delete_serializer for the Service
        if not provided then return base_serializer
        """
        if self.delete_serializer is None:
            return self.base_serializer
        else:
            return self.delete_serializer

    def delete_json_reseponse_status(self, status):
        return return_status.HTTP_204_NO_CONTENT if status else return_status.HTTP_400_BAD_REQUEST

    def delete_json_reseponse_message(self, status):
        return "Successfuly Deleted" if status else "Not Found"

    def delete(self, request, pk=None, debug=False, **kwargs):
        self.view_validator(request)
        del_model = self.get_model_delete
        pk_filed_name = self.pk_field_name_of_model(del_model)
        pk_value = request.data.get(pk_filed_name)
        obj = self.get_model_object_by_pk(pk=pk_value, model=del_model)
        status = True if obj else False
        if status:
            obj.delete()
        messages = self.delete_json_reseponse_message(status)

        return Response({"message": messages}, status=self.delete_json_reseponse_status(status))


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


class CRUDView(GetView, PostView, PutView, DeleteView, PatchView):
    pass
