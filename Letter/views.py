from Letter.models import LetterData, AttachmentType
from Letter.serializers import LetterDataSerializer, AttachmentTypeSerializer
from HelperClasses.GenericView import CRUDView
from rest_framework.views import APIView
from rest_framework.response import Response
from HelperClasses.FileUpload import File
from RTA.settings import BASE_DIR, JSON_CONFIGRATION
import os
# Create your views here.


class LetterDataView(CRUDView):
    base_model = LetterData
    base_serializer = LetterDataSerializer


class AttachmentTypeView(CRUDView):
    base_model = AttachmentType
    base_serializer = AttachmentTypeSerializer


class FileUpload(APIView):

    def post(self, request):
        print(request.FILES.get('filename').__dict__)
        for file_name, file_value in request.FILES.items():
            file_name = file_name
            extention = file_value._name.split('.')[-1]
            file_file = request.FILES[file_name]
            base_dir = os.path.join(BASE_DIR, JSON_CONFIGRATION['STATIC_DIR'])
            file_path = File.upload_file(
                file_name=file_name, extention=extention, file=file_file, base_dir=base_dir)
            print(file_path)

        return Response()
