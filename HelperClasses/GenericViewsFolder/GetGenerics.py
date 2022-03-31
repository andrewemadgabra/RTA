from rest_framework.response import Response
from rest_framework import status as return_status
from HelperClasses.GenericViewsFolder.BaseView import BaseView
from django.core.exceptions import FieldDoesNotExist
import json


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

    def get_appropriate_filtered_data(self, model, params={}, related_models=[],
                                      many_to_many_related_models=[], prefetch_related_flag=False, select_related_flag=False, all=False):
        if prefetch_related_flag:
            if all:
                data = model.objects.all().prefetch_related(*many_to_many_related_models)
            else:
                data = model.objects.filter(
                    **params).prefetch_related(*many_to_many_related_models)
        elif select_related_flag:
            if all:
                data = model.objects.all().select_related(*related_models)
            else:
                data = model.objects.filter(
                    **params).prefetch_related(*related_models)
        else:
            if all:
                data = model.objects.all()
            else:
                data = model.objects.filter(**params)

        return data

    def get_modeled_data(self, request, pk=None, model=None, field_name=None, field_value=None,
                         fields_names=[], fields_values=[], debug=False, related_models=[], many_to_many_related_models=[]):
        """
        This function is responseble for getting data from the model itself
        """
        many = True
        select_related_flag = True if len(related_models) > 0 else False
        prefetch_related_flag = True if len(
            many_to_many_related_models) > 0 else False

        if model is None:
            model = self.get_model_get
        field_name = field_name if field_name else request.GET.get(
            "field_name")
        field_value = field_value if field_value else request.GET.get(
            "field_value")

        fields_names = fields_names if fields_names else request.GET.get(
            "fields_names")
        fields_values = fields_values if fields_values else request.GET.get(
            "fields_values")

        if pk is not None:
            data = self.get_model_object_by_pk(pk=pk, model=model)
            many = False
        else:
            pk_field_name = self.pk_field_name_of_model(model=model)
            pk_field_value = request.GET.get(pk_field_name)
            if pk_field_value is not None:
                data = self.get_model_object_by_pk(
                    pk=pk_field_value, model=model)
                many = False
            elif field_name is not None:
                if field_value is None:
                    raise ValueError("field_value was not supplied.")

                params = {}
                try:
                    params[model._meta.get_field(
                        field_name).name] = json.loads(field_value)
                except FieldDoesNotExist:
                    raise ValueError(
                        "model doesn't have the field specified in field_name")

                data = self.get_appropriate_filtered_data(model=model, params=params, related_models=related_models,
                                                          many_to_many_related_models=many_to_many_related_models,
                                                          prefetch_related_flag=select_related_flag,
                                                          select_related_flag=prefetch_related_flag, all=False)

            elif fields_names:
                fields_names = fields_names.split(',')
                fields_values = fields_values.split(',')
                assert(len(fields_names) == len(fields_values)
                       ), "fields_names is not same length with fields_values"
                params = {}

                try:
                    for index, f_name in enumerate(fields_names):
                        params[model._meta.get_field(
                            f_name).name] = json.loads(fields_values[index])
                except FieldDoesNotExist:
                    raise ValueError(
                        "model doesn't have the field {}".format(f_name))

                data = self.get_appropriate_filtered_data(model=model, params=params, related_models=related_models,
                                                          many_to_many_related_models=many_to_many_related_models,
                                                          prefetch_related_flag=select_related_flag,
                                                          select_related_flag=prefetch_related_flag, all=False)

            else:
                data = self.get_appropriate_filtered_data(model=model, params={}, related_models=related_models,
                                                          many_to_many_related_models=many_to_many_related_models,
                                                          prefetch_related_flag=select_related_flag,
                                                          select_related_flag=prefetch_related_flag, all=True)
        return data, many

    def get_serialized_data(self, request, model=None, data=None, pk=None, field_name=None, field_value=None,
                            fields_names=[], fields_values=[], debug=False, many=True):
        """
        This function is responseble for getting serialized data 
        input : data -> optional, if not provided then use get_modeled_data from self. 
                        if provided then this data will be used to be serialized
        """
        if model is None:
            model = self.get_model_get
        if data is None:
            data, many = self.get_modeled_data(
                request=request, pk=pk, model=model, field_name=field_name, field_value=field_value,
                fields_names=fields_names, fields_values=fields_values, debug=debug)
        return self.get_serializer_get(data, many=many).data

    def get(self, request, pk=None, modeled_response=False,
            debug=False, data=None, many=True, **kwargs):
        if data is None:
            data, many = self.get_modeled_data(request, pk=pk, debug=debug)

        if data == None and not(many):
            return Response({}, status=return_status.HTTP_404_NOT_FOUND)

        serlized_data = self.get_serialized_data(
            request, data=data, pk=pk, debug=debug, many=many)
        return Response(serlized_data, status=return_status.HTTP_200_OK)
