

class BaseService(object):
    base_model = None
    base_serializer = None

    def validate_service(self, request):
        return

    @property
    def model(self):
        if self.base_model is None:
            raise TypeError('base_model was not provided')
        else:
            return self.base_model

    @property
    def serializer(self):
        if self.base_serializer is None:
            raise TypeError('base_serializer was not provided')
        else:
            return self.base_serializer

    def get_object(self, pk):
        try:
            obj = self.model.objects.get(pk=pk)
            return obj
        except self.model.DoesNotExist:
            return None


class GetService(BaseService):
    get_model = None
    get_serializer = None

    @property
    def get_model_get(self):
        if self.get_model is None:
            return self.model
        else:
            return self.get_model

    @property
    def get_serializer_get(self):
        if self.get_serializer is None:
            return self.serializer
        else:
            return self.get_serializer

    def get_modeled_data(self, request, *args, **kwargs):
        return self.get_model_get.objects.all()

    def get(self, request, data=None, *args, **kwargs):
        if not(data):
            data = self.get_modeled_data(request, *args, **kwargs)
        return self.get_serializer_get(data, many=True).data


class PostService(BaseService):
    post_model = None
    post_serializer = None

    @property
    def get_model_post(self):
        if self.post_model is None:
            return self.model
        else:
            return self.post_model

    @property
    def get_serializer_post(self):
        if self.post_serializer is None:
            return self.serializer
        else:
            return self.post_serializer

    def post(self, request, *args, **kwargs):
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
        if self.put_model is None:
            return self.model
        else:
            return self.put_model

    @property
    def get_serializer_put(self):
        if self.put_serializer is None:
            return self.serializer
        else:
            return self.put_serializer

    def put(self, request, *args, **kwargs):
        pk = request.data.get(self.get_model_delete._meta.pk.name)
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
        if self.delete_model is None:
            if self.base_model is None:
                raise TypeError('base_model was not provided')
            else:
                return self.base_model
        else:
            return self.delete_model

    @property
    def get_serializer_delete(self):
        if self.delete_serializer is None:
            if self.base_serializer is None:
                raise TypeError('base_serializer was not provided')
            else:
                return self.base_serializer
        else:
            return self.put_serializer

    def delete(self, request, *args, **kwargs):
        pk = request.data.get(self.get_model_delete._meta.pk.name)
        obj = self.get_model_delete.objects.filter(pk=pk)
        status = True if obj else False
        if status:
            obj.delete()
        return status


class CRUDService(GetService, PostService, PutService, DeleteService):
    pass


class CRService(GetService, PostService):
    pass
