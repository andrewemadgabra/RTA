from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels

# Create your models here.


class Jobs(AbstractDateModels):

    job_id = models.AutoField(primary_key=True)
    job_title_Ar = models.CharField(max_length=128, unique=True)
    job_title_En = models.CharField(max_length=128, unique=True)

    class Meta:
        managed = False
        db_table = 'Jobs'

    def __str__(self):
        return self.job_title_En

    def __repr__(self):
        return self.job_title_En
