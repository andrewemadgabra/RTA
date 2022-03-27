from Jobs.models import Jobs
from Jobs.serializers import JobsSerializer
from HelperClasses.GenericService import CRUDService


class JobsService(CRUDService):
    base_model = Jobs
    base_serializer = JobsSerializer

