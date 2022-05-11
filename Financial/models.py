from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator


class FinancialClaimsStatus(AbstractDateModels):
    financial_claims_status_id = models.AutoField(primary_key=True)
    financial_claims_status_Ar = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    financial_claims_status_En = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'FinancialClaimsStatus'
        ordering = ('financial_claims_status_id',)

    def __str__(self):
        return self.financial_claims_status_En

    def __repr__(self):
        return self.financial_claims_status_En
