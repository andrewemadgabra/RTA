from Letter.models import LetterData, AttachmentType, LetterAttachments
from Letter.serializers import LetterDataSerializer, AttachmentTypeSerializer, LetterAttachmentsSerializer
from HelperClasses.GenericView import CRUDView
from rest_framework.views import APIView
from rest_framework.response import Response
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
            letter_data_saved = LetterData.objects.create(**{"issued_number": letter_object.validated_data.get(
                "issued_number"), "letter_title":  letter_object.validated_data.get("letter_title"), "action_user": User.objects.get(pk=1)})
            letter_data = LetterDataSerializer(letter_data_saved)
            return letter_data.data, True
        return letter_object.errors, False

    def attachment_data_handler(self, files, letter_data):
        letter_data = LetterData.objects.get(
            letter_data_id=letter_data.get('letter_data_id'))
        saved_files = []
        files_data = []
        for file_name, file_value in files.items():
            new_file_name, extention = File.get_new_file_name_with_extenstion(
                file_value.name)

            att = AttachmentType.objects.get(content_type=extention)
            letter_attachment = {"letter_data": letter_data.letter_data_id, "letter_attach_name": file_value.name,
                                 "file_path_on_server": new_file_name, "attachment_type": att.attachment_type_id, }
            valid_attachment = LetterAttachmentsSerializer(
                data=letter_attachment)
            if valid_attachment.is_valid():
                letter_attach_saved = LetterAttachments.objects.create(**{'letter_data': letter_data,
                                                                          'letter_attach_name': valid_attachment.validated_data.get('letter_attach_name'),
                                                                          'file_path_on_server':  valid_attachment.validated_data.get('file_path_on_server'),
                                                                          'attachment_type':  att})
                files_data.append(LetterAttachmentsSerializer(
                    letter_attach_saved).data)

                ##### phiscal upload step #######
                File.upload_file(**{
                    "file_name": new_file_name,
                    "extention":  extention,
                    "file": files[file_name],
                    "base_dir": os.path.join(BASE_DIR, JSON_CONFIGRATION['STATIC_DIR'])
                })
                ##### end of phiscal upload #######
                saved_files.append(new_file_name)
            else:
                [os.remove(os.path.join(JSON_CONFIGRATION['STATIC_DIR'], new_file_name))
                 for new_file_name in saved_files]
                return valid_attachment.errors, False

        return files_data, True

    @transaction.atomic
    def post(self, request, modeled_response=False, debug=False, **kwargs):
        self.view_validator(request)
        files = request.FILES
        data = request.data

        return_attachment = []

        letter_data, status = self.letter_data_handler(data)
        if status:
            return_attachment, status = self.attachment_data_handler(
                files, letter_data)
            return_status = self.post_json_reseponse_status(status)

        return Response({"data": letter_data, "attachment": return_attachment}, status=return_status)


class AttachmentTypeView(CRUDView):
    base_model = AttachmentType
    base_serializer = AttachmentTypeSerializer


class FileUpload(APIView):

    def post(self, request):
        print(request.FILES.get('filename').__dict__)
        print(request.data)

        return Response()
