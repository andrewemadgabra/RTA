from Letter.models import LetterData, AttachmentType
from Letter.serializers import LetterDataSerializer, AttachmentTypeSerializer
from HelperClasses.GenericView import CRUDView
# Create your views here.


class LetterDataView(CRUDView):
    base_model = LetterData
    base_serializer = LetterDataSerializer


class AttachmentTypeView(CRUDView):
    base_model = AttachmentType
    base_serializer = AttachmentTypeSerializer
