from rest_framework.response import Response
from rest_framework import status as return_status
from HelperClasses.GenericViewsFolder.BaseView import BaseView


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
