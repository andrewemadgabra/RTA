from HelperClasses.AbstractDateModels import AbstractDateModels
from django.db import models
from HelperClasses.DjangoValidator import DjangoValidator
# Create your models here.


class DeliveryMethod(AbstractDateModels):
    delivery_method_id = models.AutoField(primary_key=True)
    delivery_method_name_ar = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    delivery_method_name_en = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'DeliveryMethod'
        ordering = ('delivery_method_id',)

    def __str__(self):
        return self.delivery_Method_name_en

    def __repr__(self):
        return self.delivery_Method_name_en


class PriorityLevel(AbstractDateModels):
    priority_level_id = models.AutoField(primary_key=True)
    priority_level_ar = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    priority_level_en = models.CharField(max_length=128, unique=True,  validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'PriorityLevel'
        ordering = ('priority_level_id',)

    def __str__(self):
        return self.priority_level_en

    def __repr__(self):
        return self.priority_level_en
