from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator


class Projects(AbstractDateModels):
    project_id = models.AutoField(primary_key=True)
    project_Ar = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    project_En = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'Projects'
        ordering = ('project_id',)

    def __str__(self):
        return self.project_En

    def __repr__(self):
        return self.project_En


class ProjectSections(AbstractDateModels):
    project_section_id = models.AutoField(primary_key=True)
    project_section_Ar = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    project_section_En = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_EnglishLetters])
    project = models.ForeignKey(
        Projects, models.CASCADE, related_name="section_project", db_column="project_id")

    class Meta:
        managed = False
        db_table = 'ProjectSections'
        ordering = ('project_section_id',)

    def __str__(self):
        return self.project_section_En

    def __repr__(self):
        return self.project_section_En


class ProjectContracts(AbstractDateModels):
    project_contract_id = models.AutoField(primary_key=True)
    project_contract_num = models.CharField(max_length=512)
    project_section = models.ForeignKey(
        ProjectSections, models.CASCADE, related_name="contract_pro_section", db_column="project_section_id")

    class Meta:
        managed = False
        db_table = 'ProjectContracts'
        ordering = ('project_contract_id',)

    def __str__(self):
        return self.project_contract_En

    def __repr__(self):
        return self.project_contract_En


