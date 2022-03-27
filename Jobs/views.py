from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Jobs.jobs_service import JobsService
from HelperClasses.GenericView import CRUDView

# Create your views here.


class JobsView(CRUDView):
    base_service = JobsService

