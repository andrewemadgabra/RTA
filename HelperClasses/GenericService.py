

class BaseService(object):
    base_model = None
    base_serializer = None

    def validate_service(self, request):
        """
        This function responseble for makeing validataion
        input ->  request object
        """
        return

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

    def get_object(self, pk, model=None):
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
            return None

    def get_primary_key_field(self, model):
        if not(model):
            model = self.base_model
        for field in model._meta.fields:
            if field.primary_key:
                return field.name


class GetService(BaseService):
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

    def get_modeled_data(self, request, *args, **kwargs):
        """
        This function is responseble for getting data from the model itself
        """
        return self.get_model_get.objects.all()

    def get(self, request, data=None, *args, **kwargs):
        """
        This function is responseble for getting serialized data 
        input : data -> optional, if not provided then use get_modeled_data from self. 
                        if provided then this data will be used to be serialized
        """
        if not(data):
            data = self.get_modeled_data(request, *args, **kwargs)
        return self.get_serializer_get(data, many=True).data


class PostService(BaseService):
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

    def post(self, request, *args, **kwargs):
        """
        This function is reseponseble for create new object from the model given.
        The model can be get_model_post if not existed  then use base_model.

        This function return seralized data or error , and status (bool) to identifiy whethere it successfully created 
        or not.
        """
        self.validate_service(request)
        object_to_save = self.get_serializer_post(
            data=request.data)
        if object_to_save.is_valid():
            object_to_save.save()
            return object_to_save.data, True
        else:
            return object_to_save.errors, False


class PutService(BaseService):
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

    def put(self, request, *args, **kwargs):
        pk = self.get_primary_key_field(self.get_model_put)
        pk = request.data.get(pk)
        obj = self.get_object(pk=pk)
        if not(obj):
            return {"error": ["Object Not Found"]}, False
        object_to_save = self.get_serializer_put(instance=obj,
                                                 data=request.data)
        if object_to_save.is_valid():
            object_to_save.save()
            return object_to_save.data, True
        else:
            return object_to_save.errors, False


class DeleteService(BaseService):
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

    def delete(self, request, *args, **kwargs):
        pk = request.data.get(self.get_model_delete._meta.pk.name)
        obj = self.get_model_delete.objects.filter(pk=pk)
        status = True if obj else False
        if status:
            obj.delete()
        return status


class PatchService(BaseService):

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
            return self.patch_serializer

    def patch(self, request, *args, **kwargs):
        pk = self.get_primary_key_field(self.get_model_patch)
        pk = request.data.get(pk)
        obj = self.get_object(pk=pk)
        if not(obj):
            return {"error": ["Object Not Found"]}, False

        fields = list(self.get_model_patch._meta.fields)
        new_data = {}
        for field in fields:
            new_data[field.name] = request.data.get(
                field.name, getattr(obj, field.name))

        request._full_data = new_data

        object_to_save = self.get_serializer_patch(instance=obj,
                                                   data=request.data)
        if object_to_save.is_valid():
            object_to_save.save()
            return object_to_save.data, True
        else:
            return object_to_save.errors, False


class CRUDService(GetService, PostService, PutService, DeleteService, PatchService):
    pass


class CRService(GetService, PostService):
    pass
