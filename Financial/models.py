from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator
from Actors.models import SubActors


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


class FinancialClaims(AbstractDateModels):
    financial_claims_id = models.AutoField(primary_key=True)
    target = models.CharField(max_length=512)
    value = models.DecimalField(max_digits=18, decimal_places=2)
    financial_claims_status = models.ForeignKey(
        FinancialClaimsStatus, models.CASCADE, related_name="financial_claims_status",
        db_column="financial_claims_status_id")

    class Meta:
        managed = False
        db_table = 'FinancialClaims'
        ordering = ('financial_claims_id',)

    def __str__(self):
        return self.target

    def __repr__(self):
        return self.target
