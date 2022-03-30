from Periority.models import DeliveryMethod, AttachmentType, PriorityLevel
from Periority.serializers import (DeliveryMethodSerializer,
                                   PriorityLevelSerializer)
from HelperClasses.GenericView import CRUDView

# Create your views here.


class DeliveryMethodView(CRUDView):
    base_model = DeliveryMethod
    base_serializer = DeliveryMethodSerializer


class PriorityLevelView(CRUDView):
    base_model = PriorityLevel
    base_serializer = PriorityLevelSerializer
