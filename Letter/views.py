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

    def letter_data_handler(self, data):
        b_serializer = self.serializer
        letter_object = b_serializer(data={"issued_number":  data.get('issued_number'),
                                           "letter_title":  data.get('letter_title'),
                                           "action_user":  1
                                           }
                                     )

        if letter_object.is_valid():
            return letter_object.data, True
        return letter_object.errors, False

    def attachment_data_handler(self, files, letter_data):
        return_attachment_to_upload = []
        return_attachment_to_save = []
        pk_of_attachment_type = {}
        for file_name, file_value in files.items():
            new_file_name, extention = File.get_new_file_name_with_extenstion(
                file_value.name)
            return_attachment_to_upload.append(
                {
                    "file_name": new_file_name,
                    "extention":  extention,
                    "file": files[file_name],
                    "base_dir": os.path.join(BASE_DIR, JSON_CONFIGRATION['STATIC_DIR'])
                }
            )
            att = AttachmentType.objects.get(content_type=extention)
            return_attachment_to_save.append(
                {
                    "letter_data": letter_data['letter_data_id'],
                    "letter_attach_name": file_name,
                    "file_path_on_server": new_file_name,
                    "attachment_type": att.attachment_type_id,
                    "attachment_type_obj": att
                }
            )

        return return_attachment_to_upload, return_attachment_to_save

    def save_attachment_to_upload(self, attachments, letter_data):
        valid_attachment = LetterAttachmentsSerializer(
            data=attachments, many=True)
        if valid_attachment.is_valid():
            for attachment in attachments:
                LetterAttachments.objects.create(**{"letter_data": letter_data, "letter_attach_name": attachment.get(
                    'letter_attach_name'), "file_path_on_server": attachment.get('file_path_on_server'), "attachment_type": attachment.get('attachment_type_obj')})
            return valid_attachment.data, True
        return valid_attachment.errors, False

    def upload_attachment_to_save(self, attachments):
        for attachment in attachments:
            File.upload_file(**attachment)

    @transaction.atomic
    def post(self, request, modeled_response=False, debug=False, **kwargs):
        self.view_validator(request)
        files = request.FILES
        data = request.data

        letter_data, status = self.letter_data_handler(data)
        if status:
            letter_data_saved = LetterData.objects.create(**{"issued_number": letter_data.get(
                "issued_number"), "letter_title":  letter_data.get("letter_title"), "action_user": User.objects.get(pk=1)})
            letter_data = LetterDataSerializer(letter_data_saved).data

            return_attachment_to_upload, return_attachment_to_save = self.attachment_data_handler(
                files, letter_data)

            attatchments, a_status = self.save_attachment_to_upload(
                return_attachment_to_save, letter_data=letter_data_saved)

            self.upload_attachment_to_save(return_attachment_to_upload)

        return Response({"data": letter_data, "attachment": attatchments}, status=return_status.HTTP_201_CREATED)


class AttachmentTypeView(CRUDView):
    base_model = AttachmentType
    base_serializer = AttachmentTypeSerializer


class FileUpload(APIView):

    def post(self, request):
        print(request.FILES.get('filename').__dict__)
        print(request.data)

        return Response()
