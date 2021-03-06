from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator
# Create your models here.


class EmploymentStatus(AbstractDateModels):

    employment_id = models.AutoField(primary_key=True)
    employment_title_Ar = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    employment_title_En = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'EmploymentStatus'
        ordering = ('employment_id',)

    def __str__(self):
        return self.employment_title_En

    def __repr__(self):
        return self.employment_title_En
