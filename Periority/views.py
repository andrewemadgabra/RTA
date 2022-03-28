from Periority.models import DeliveryMethod, AttachmentType, PriorityLevel
from Periority.serializers import (DeliveryMethodSerializer, AttachmentTypeSerializer,
                                   PriorityLevelSerializer)
from HelperClasses.GenericView import CRUDView

# Create your views here.


class DeliveryMethodView(CRUDView):
    base_model = DeliveryMethod
    base_serializer = DeliveryMethodSerializer


class AttachmentTypeView(CRUDView):
    base_model = AttachmentType
    base_serializer = AttachmentTypeSerializer


class PriorityLevelView(CRUDView):
    base_model = PriorityLevel
    base_serializer = PriorityLevelSerializer
