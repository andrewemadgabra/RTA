from rest_framework.response import Response
from rest_framework import status as return_status
from HelperClasses.GenericViewsFolder.BaseView import BaseView


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
