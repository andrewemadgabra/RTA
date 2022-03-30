from Letter.models import LetterData, AttachmentType, LetterAttachments
from Letter.serializers import LetterDataSerializer, AttachmentTypeSerializer, LetterAttachmentsSerializer
from HelperClasses.GenericView import CRUDView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as return_status
from HelperClasses.FileUpload import File
from RTA.settings import BASE_DIR, JSON_CONFIGRATION
import os
from django.db import transaction
from User.models import User
# Create your views here.


class LetterDataView(CRUDView):
    base_model = LetterData
    base_serializer = LetterDataSerializer
    post_model = LetterAttachments
    post_serializer = LetterAttachmentsSerializer

    @transaction.atomic
    def post(self, request, modeled_response=False, debug=False, **kwargs):
        self.view_validator(request)
        files = request.FILES
        data = request.data
        try:
            issued_number = data["issued_number"]
            letter_title = data["letter_title"]
            attachment_types = eval(data["attachment_type"])
            action_user = User.objects.get(pk=1)

            assert(int(issued_number) > 0), "not a valid issued_number"
            assert(type(letter_title) == str and len(
                letter_title) < 256), "no a valid letter_title"
            assert(len(attachment_types) == len(files))
        except Exception as e:
            return Response({"error": [e.__str__()]})

        p_model = self.model
        saved_object = p_model.objects.create(
            issued_number=issued_number, letter_title=letter_title, action_user=action_user)

        for index, value in enumerate(files.items()):
            file_name, file_value = value
            file_name = file_name
            extention = file_value._name.split('.')[-1]
            file_file = files[file_name]
            base_dir = os.path.join(BASE_DIR, JSON_CONFIGRATION['STATIC_DIR'])
            _, file_path = File.upload_file(
                file_name=file_name, extention=extention, file=file_file, base_dir=base_dir)
            LetterAttachments.objects.create(letter_data_id=saved_object.letter_data_id, letter_attach_name=file_name,
                                             file_path_on_server=file_path, attachment_type_id=attachment_types[index])

        object_after__insert = p_model.objects.get(
            letter_data_id=saved_object.letter_data_id)
        p_serializer = self.serializer
        serialized_data = p_serializer(object_after__insert).data
        p_in_model = self.get_model_post
        p_in_serializer = self.get_serializer_post
        attatchments = p_in_model.objects.filter(
            letter_data=object_after__insert.letter_data_id)
        serialized_att = p_in_serializer(attatchments, many=True).data

        return Response({"data": serialized_data, "attachment": serialized_att}, status=return_status.HTTP_201_CREATED)


class AttachmentTypeView(CRUDView):
    base_model = AttachmentType
    base_serializer = AttachmentTypeSerializer


class FileUpload(APIView):

    def post(self, request):
        print(request.FILES.get('filename').__dict__)
        print(request.data)

        return Response()
