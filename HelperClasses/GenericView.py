from importlib_metadata import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class BaseView(APIView):
    base_model = None
    base_serializer = None
    base_service = None

    @property
    def model(self):
        if self.base_model is None:
            raise TypeError('base_model was not provided')
        return self.base_model

    @property
    def serializer(self):
        if self.base_serializer is None:
            raise TypeError('base_serializer was not provided')
        return self.base_serializer

    @property
    def service(self):
        if self.base_service is None:
            raise TypeError('base_service was not provided')
        return self.base_service

    def view_validator(self, request):
        return None


class GetView(BaseView):
    get_model = None
    get_serializer = None
    get_service = None

    @property
    def get_model_get(self):
        if self.get_model is None:
            return self.model
        return self.get_model

    @property
    def get_serializer_get(self):
        if self.get_serializer is None:
            return self.serializer
        return self.get_serializer

    @property
    def get_service_get(self):
        if self.get_service is None:
            return self.service
        return self.get_service

    def get(self, request, *args, **kwargs):
        return Response(self.get_service_get().get(request, *args, **kwargs), status=status.HTTP_200_OK)


class PostView(BaseView):
    post_model = None
    post_serializer = None
    post_service = None

    @property
    def get_model_post(self):
        if self.post_model is None:
            return self.model
        return self.post_model

    @property
    def get_serializer_post(self):
        if self.post_serializer is None:
            return self.serializer
        return self.post_serializer

    @property
    def get_service_post(self):
        if self.post_service is None:
            return self.service
        return self.post_service

    def post(self, request, *args, **kwargs):
        self.view_validator(request)
        ouput, returned_stutus = self.get_service_post().post(request, *args, **kwargs)
        returned_stutus = status.HTTP_201_CREATED if returned_stutus else status.HTTP_400_BAD_REQUEST
        return Response(ouput, status=returned_stutus)


class PutView(BaseView):
    put_model = None
    put_serializer = None
    put_service = None

    @property
    def get_model_put(self):
        if self.put_model is None:
            return self.model
        return self.put_model

    @property
    def get_serializer_put(self):
        if self.put_serializer is None:
            return self.serializer
        return self.put_serializer

    @property
    def get_service_put(self):
        if self.put_service is None:
            return self.service
        return self.put_service

    def put(self, request, *args, **kwargs):
        self.view_validator(request)
        ouput, returned_stutus = self.get_service_put().put(request, *args, **kwargs)
        returned_stutus = status.HTTP_200_OK if returned_stutus else status.HTTP_400_BAD_REQUEST
        return Response(ouput, status=returned_stutus)


class DeleteView(BaseView):
    delete_model = None
    delete_serializer = None
    delete_service = None

    @property
    def get_model_delete(self):
        if self.delete_model is None:
            return self.model
        return self.delete_model

    @property
    def get_serializer_delete(self):
        if self.delete_serializer is None:
            return self.serializer
        return self.delete_serializer

    @property
    def get_service_delete(self):
        if self.delete_service is None:
            return self.service
        return self.delete_service

    def delete(self, request, *args, **kwargs):
        self.view_validator(request)
        return_status = self.get_service_delete().delete(request, *args, **kwargs)
        messages = "Successfuly Deleted" if return_status else "Not Found"
        return_status = status.HTTP_204_NO_CONTENT if return_status else status.HTTP_400_BAD_REQUEST
        return Response({"message": messages}, status=return_status)


class PatchView(BaseView):
    patch_model = None
    patch_serializer = None
    patch_service = None

    @property
    def get_model_patch(self):
        if self.patch_model is None:
            return self.model
        return self.patch_model

    @property
    def get_serializer_patch(self):
        if self.patch_serializer is None:
            return self.serializer
        return self.patch_serializer

    @property
    def get_service_patch(self):
        if self.patch_service is None:
            return self.service
        return self.patch_service

    def patch(self, request, *args, **kwargs):
        self.view_validator(request)
        ouput, returned_stutus = self.get_service_patch().patch(
            request, *args, **kwargs)
        returned_stutus = status.HTTP_200_OK if returned_stutus else status.HTTP_400_BAD_REQUEST
        return Response(ouput, status=returned_stutus)


class CRUDView(GetView, PostView, PutView, DeleteView, PatchView):
    pass
