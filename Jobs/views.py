from Jobs.models import Jobs
from Jobs.serializers import JobsSerializer
from HelperClasses.GenericView import CRUDView

# Create your views here.


class JobsView(CRUDView):
    base_model = Jobs
    base_serializer = JobsSerializer
