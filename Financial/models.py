from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator
from Actors.models import SubActors
from Letter.models import LetterData


class FinancialClaimsStatus(AbstractDateModels):
    financial_claims_status_id = models.AutoField(primary_key=True)
    financial_claims_status_Ar = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    financial_claims_status_En = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'FinancialClaimsStatus'

    def __str__(self):
        return self.financial_claims_status_En

    def __repr__(self):
        return self.financial_claims_status_En


class FinancialClaims(AbstractDateModels):
    financial_claims_id = models.AutoField(primary_key=True)
    target = models.CharField(max_length=512, validators=[
            DjangoValidator().validation_ArabicLettersOrNumbers])
    value = models.FloatField()
    financial_claims_status = models.ForeignKey(
        FinancialClaimsStatus, models.CASCADE, related_name="financial_claims_status", 
        db_column="financial_claims_status_id")
    sub_actor = models.ForeignKey(
        SubActors, models.CASCADE, related_name="fcs_subactor", 
        db_column="sub_actor_id")
    letter_data = models.ForeignKey(
        LetterData, models.CASCADE, related_name="fcs_letter_data", 
        db_column="letter_data_id")

    class Meta:
        managed = False
        db_table = 'FinancialClaims'

    def __str__(self):
        return self.target

    def __repr__(self):
        return self.target
