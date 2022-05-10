from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from User.models import User
from Topics.models import TopicSubcategories
from Projects.models import ProjectSections
from Actors.models import SubActors
from Periority.models import DeliveryMethod
from Financial.models import FinancialClaims
from HelperClasses.DjangoValidator import DjangoValidator


class LetterData(AbstractDateModels):
    letter_data_id = models.AutoField(primary_key=True)
    issued_number = models.PositiveIntegerField()
    letter_title = models.CharField(max_length=256)
    action_user = models.ForeignKey(
        User, models.CASCADE, related_name="creator_letter", db_column="action_user")
    topic_subcategories = models.ForeignKey(
        TopicSubcategories, models.CASCADE, blank=True, null=True)
    sub_actor_sender = models.ForeignKey(SubActors, models.CASCADE)
    sub_actor_resciver = models.ForeignKey(SubActors, models.CASCADE)
    delivery_user = models.ForeignKey(User, models.CASCADE)
    delivery_method = models.ForeignKey(DeliveryMethod, models.CASCADE)
    project_section = models.ForeignKey(
        ProjectSections, models.CASCADE, blank=True, null=True)
    subject_text = models.CharField(max_length=1000)
    financial_claims = models.ForeignKey(
        FinancialClaims, models.CASCAD, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "LetterData"
        ordering = ('letter_data_id',)

    def __str__(self):
        return self.letter_title

    def __repr__(self):
        return self.letter_title


class AttachmentType(AbstractDateModels):
    attachment_type_ar = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    attachment_type_en = models.CharField(max_length=128, validators=[
        DjangoValidator().validation_EnglishLetters])

    content_type = models.CharField(max_length=128, primary_key=True)
    charset = models.CharField(max_length=128, null=True, blank=True)
    max_size = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'AttachmentType'
        ordering = ('created_at',)

    def __str__(self):
        return self.attachment_type_en

    def __repr__(self):
        return self.attachment_type_en


class LetterAttachments(AbstractDateModels):
    letter_attachment_id = models.AutoField(primary_key=True)
    letter_data = models.ForeignKey(LetterData, models.CASCADE)
    letter_attach_name = models.CharField(max_length=128)
    file_path_on_server = models.CharField(max_length=128)
    attachment_type = models.ForeignKey(
        AttachmentType, models.CASCADE, db_column='content_type')

    class Meta:
        managed = False
        db_table = 'LetterAttachemnets'
        ordering = ('letter_attachment_id',)

    def __str__(self):
        return self.letter_attach_name

    def __repr__(self):
        return self.letter_attach_name
