from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
# Create your models here.


class EmploymentStatus(AbstractDateModels):

    employment_id = models.AutoField(primary_key=True)
    employment_title_Ar = models.CharField(max_length=128, unique=True)
    employment_title_En = models.CharField(max_length=128, unique=True)

    class Meta:
        managed = False
        db_table = 'EmploymentStatus'

    def __str__(self):
        return self.employment_title_En


