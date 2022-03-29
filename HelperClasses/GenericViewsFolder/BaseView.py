from rest_framework.views import APIView


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
