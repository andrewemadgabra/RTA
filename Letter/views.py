from Letter.models import LetterData, AttachmentType, LetterAttachments, LetterStatus, LetterDataLogger
from Letter.letterlogger import LetterLogger
from Letter.serializers import LetterDataSerializer, AttachmentTypeSerializer, LetterAttachmentsSerializer
from HelperClasses.GenericView import CRUDView
from HelperClasses.DateTimeHandler import DateTimeHandler
from rest_framework.response import Response
from HelperClasses.FileUpload import File
from RTA.settings import BASE_DIR, JSON_CONFIGRATION
import os
from django.db import transaction, IntegrityError
from User.models import User
from Topics.models import TopicSubcategories
from Actors.models import SubActors
from Periority.models import DeliveryMethod
from Projects.models import ProjectSections
from Financial.models import FinancialClaimsStatus
# Create your views here.


class LetterDataView(CRUDView):
    base_model = LetterData
    base_serializer = LetterDataSerializer
    post_model = LetterAttachments
    post_serializer = LetterAttachmentsSerializer

    def get(self, request, pk=None, modeled_response=False,
            debug=False, data=None, many=True, **kwargs):

        data, many = self.get_modeled_data(request, pk=pk, debug=debug)
        serlized_data = self.get_serialized_data(
            request, data=data, pk=pk, debug=debug, many=many)
        if not(many) and data is not None:
            attachments = LetterAttachments.objects.filter(
                letter_data=serlized_data.get('letter_data_id'))
            attachments = LetterAttachmentsSerializer(
                attachments, many=True).data
            serlized_data = {"letter": serlized_data,
                             "attachment": attachments}

        return_status = self.get_returned_status(
            True if data is not None else False)
        return Response(serlized_data, status=return_status)

    def get_logger_message(self, username, user_id, action_name, letter_id, from_status, to_status, is_initial):
        return ("{} with user_id of {} has made {} to change letter_id {}  from status {}  to status {}"
                .format(username, user_id, action_name, letter_id, from_status, to_status)
                if is_initial
                else "{} with user_id of {} has made {} to start letter_id {} with to status {}"
                .format(username, user_id, action_name, letter_id, to_status))

    def letter_data_handler(self, data):
        b_serializer = self.serializer
        letter_object = b_serializer(data={"issued_number":  data.get('issued_number'),
                                           "letter_title":  data.get('letter_title'),
                                           "action_user":  1,
                                           "topic_subcategories":  data.get('topic_subcategories'),
                                           "sub_actor_sender":  data.get('sub_actor_sender'),
                                           "sub_actor_receiver": data.get('sub_actor_receiver'),
                                           "delivery_user":  data.get('delivery_user'),
                                           "delivery_method":  data.get('delivery_method'),
                                           "project_section":  data.get("project_section"),
                                           "subject_text":  data.get('subject_text'),
                                           "financial_target": data.get("financial_target"),
                                           "financial_value":  data.get("financial_value"),
                                           "financial_claims_status":  data.get("financial_claims_status"),
                                           "issued_date":  DateTimeHandler.string_to_date(data.get("issued_date"))
                                           }
                                     )
        if letter_object.is_valid():
            user_object = User.objects.get(pk=1)
            letter_data_saved = LetterData.objects.create(**{
                "issued_number": letter_object.validated_data.get("issued_number"),
                "letter_title":  letter_object.validated_data.get("letter_title"),
                "action_user": user_object,
                # None if letter_object.validated_data.get("topic_subcategories") == None else TopicSubcategories.objects.get(pk=letter_object.validated_data.get("topic_subcategories")),
                "topic_subcategories":  letter_object.validated_data.get("topic_subcategories"),
                # SubActors.objects.get(pk=letter_object.validated_data.get("sub_actor_sender")),
                "sub_actor_sender": letter_object.validated_data.get("sub_actor_sender"),
                # SubActors.objects.get(pk=letter_object.validated_data.get("sub_actor_resciver")),
                "sub_actor_receiver": letter_object.validated_data.get("sub_actor_receiver"),
                # User.objects.get(pk=letter_object.validated_data.get("delivery_user")),
                "delivery_user":  letter_object.validated_data.get("delivery_user"),
                # DeliveryMethod.objects.get(pk=letter_object.validated_data.get("delivery_method")),
                "delivery_method":  letter_object.validated_data.get("delivery_method"),
                # None if letter_object.validated_data.get("project_section") == None else ProjectSections.objects.get(pk=letter_object.validated_data.get("project_section")),
                "project_section": letter_object.validated_data.get("project_section"),
                "subject_text":  letter_object.validated_data.get("subject_text"),
                # None if letter_object.validated_data.get("financial_claims") == None else FinancialClaims.objects.get(pk=letter_object.validated_data.get("financial_claims"))
                "financial_target":  letter_object.validated_data.get("financial_target"),
                "financial_value": letter_object.validated_data.get("financial_value"),
                "financial_claims_status": letter_object.validated_data.get("financial_claims_status"),
                "issued_date":  letter_object.validated_data.get("issued_date"),
                "letter_status": LetterStatus.objects.get(letter_status_id=1)
            })
            (LetterLogger.create_log(
                log_message=self.get_logger_message(username=user_object.username, user_id=user_object.id,
                                                    action_name='Initiate creation', letter_id=letter_data_saved.letter_data_id,
                                                    from_status=None, to_status=1, is_initial=True),
                letter_object=letter_data_saved,
                user_object=user_object,
                from_status_object=None,
                to_status=LetterStatus.objects.get(letter_status_id=1),
            ))
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
            letter_attachment = {"letter_data": letter_data.letter_data_id, "letter_attach_name": file_value.name,
                                 "file_path_on_server": new_file_name, "attachment_type": extention, }
            valid_attachment = LetterAttachmentsSerializer(
                data=letter_attachment)
            if valid_attachment.is_valid():
                letter_attach_saved = LetterAttachments.objects.create(**{'letter_data': letter_data,
                                                                          'letter_attach_name': valid_attachment.validated_data.get('letter_attach_name'),
                                                                          'file_path_on_server':  valid_attachment.validated_data.get('file_path_on_server'),
                                                                          'attachment_type':  AttachmentType.objects.get(content_type=valid_attachment.validated_data.get("attachment_type"))})
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

    def post(self, request, modeled_response=False, debug=False, **kwargs):
        self.view_validator(request)
        files = request.FILES
        data = request.data

        return_attachment = []
        letter_data = {}
        try:
            with transaction.atomic():
                letter_data, status = self.letter_data_handler(data)
                if status:
                    return_attachment, status = self.attachment_data_handler(
                        files, letter_data)
                if not(status):
                    raise IntegrityError
        except IntegrityError:
            status = False
        except TypeError:
            status = False

        return_status = self.post_json_reseponse_status(status)

        return Response({"letter": letter_data, "attachment": return_attachment}, status=return_status)


class AttachmentTypeView(CRUDView):
    base_model = AttachmentType
    base_serializer = AttachmentTypeSerializer
