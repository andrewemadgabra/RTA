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

    def get_attachment_id(self, extention):
        try:
            return AttachmentType.objects.get(content_type=extention)
        except AttachmentType.DoesNotExist:
            return None

    def letter_data_handler(self, data):
        b_serializer = self.serializer
        letter_object = b_serializer(data={"issued_number":  data.get('issued_number'),
                                           "letter_title":  data.get('letter_title'),
                                           "action_user":  1
                                           }
                                     )

        if letter_object.is_valid():
            return letter_object.data, True
        return letter_object.erros, False

    def attachment_data_handler(self, files, letter_data):
        return_attachment_to_upload = []
        return_attachment_to_save = []
        pk_of_attachment_type = {}
        for file_name, file_value in files.items():
            new_file_name, extention = File.get_new_file_name_with_extenstion(
                file_value._name)
            return_attachment_to_upload.append(
                {
                    "file_name": new_file_name,
                    "extention":  extention,
                    "file_file": files[file_name],
                    "base_dir": os.path.join(BASE_DIR, JSON_CONFIGRATION['STATIC_DIR'])
                }
            )
            selized_attachment = AttachmentTypeSerializer(
                self.get_attachment_id(extention))

            return_attachment_to_save.append(
                {
                    "letter_data_id": letter_data.letter_data_id,
                    "letter_attach_name": file_name,
                    "file_path_on_server": new_file_name,
                    "attachment_type": pk_of_attachment_type.get(extention)
                }
            )

            # LetterAttachments.objects.create(letter_data_id=,=,
            #                                  =, attachment_type_id=AttachmentType.objects.get(content_type=extention).pk)

        return [], []

    # @transaction.atomic
    # def post(self, request, modeled_response=False, debug=False, **kwargs):
    #     self.view_validator(request)
    #     files = request.FILES
    #     data = request.data

    #     letter_data, status = self.letter_data_handler(data)

    #     _, file_path = File.upload_file(
    #         file_name=file_name, extention=extention, file=file_file, base_dir=base_dir)

    #     object_after__insert = p_model.objects.get(
    #         letter_data_id=saved_object.letter_data_id)
    #     p_serializer = self.serializer
    #     serialized_data = p_serializer(object_after__insert).data
    #     p_in_model = self.get_model_post
    #     p_in_serializer = self.get_serializer_post
    #     attatchments = p_in_model.objects.filter(
    #         letter_data=object_after__insert.letter_data_id)
    #     serialized_att = p_in_serializer(attatchments, many=True).data

    #     return Response({"data": serialized_data, "attachment": serialized_att}, status=return_status.HTTP_201_CREATED)


class AttachmentTypeView(CRUDView):
    base_model = AttachmentType
    base_serializer = AttachmentTypeSerializer


class FileUpload(APIView):

    def post(self, request):
        print(request.FILES.get('filename').__dict__)
        print(request.data)

        return Response()
