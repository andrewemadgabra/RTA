from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator

# Create your models here.


class Jobs(AbstractDateModels):

    job_id = models.AutoField(primary_key=True)
    job_title_Ar = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    job_title_En = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'Jobs'
        ordering = ('job_id',)

    def __str__(self):
        return self.job_title_En

    def __repr__(self):
        return self.job_title_En
