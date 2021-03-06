from turtle import mode
from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator
from User.models import User
from Topics.models import TopicSubcategories
from Projects.models import ProjectSections
from Actors.models import SubActors
from Periority.models import DeliveryMethod
from Financial.models import FinancialClaimsStatus


class LetterStatus(AbstractDateModels):
    letter_status_id = models.AutoField(primary_key=True)
    letter_status_group = models.PositiveIntegerField()
    letter_status_description_ar = models.CharField(
        max_length=1024, validators=[DjangoValidator.validation_ArabicLettersOrNumbers])
    letter_status_description_en = models.CharField(
        max_length=1024, validators=[DjangoValidator.validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = "LetterStatus"
        ordering = ('letter_status_id',)

    def __str__(self):
        return self.letter_status_description_en

    def __repr__(self):
        return self.letter_status_description_en


class LetterData(AbstractDateModels):
    letter_data_id = models.AutoField(primary_key=True)
    issued_number = models.PositiveIntegerField()
    letter_title = models.CharField(max_length=256)
    action_user = models.ForeignKey(
        User, models.CASCADE, related_name="creator_letter", db_column="action_user")
    topic_subcategories = models.ForeignKey(
        TopicSubcategories, models.CASCADE, blank=True, null=True)
    sub_actor_sender = models.ForeignKey(
        SubActors, models.CASCADE, related_name="sub_actor_sender", db_column="sub_actor_sender_id")
    sub_actor_receiver = models.ForeignKey(
        SubActors, models.CASCADE, related_name="sub_actor_receiver", db_column="sub_actor_receiver_id")
    delivery_user = models.ForeignKey(User, models.CASCADE)
    delivery_method = models.ForeignKey(DeliveryMethod, models.CASCADE)
    project_section = models.ForeignKey(
        ProjectSections, models.CASCADE, blank=True, null=True)
    subject_text = models.CharField(max_length=1000)
    financial_target = models.CharField(max_length=512, null=True, blank=True)
    financial_value = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True)
    financial_claims_status = models.ForeignKey(
        FinancialClaimsStatus, models.CASCADE, related_name="financial_claims_status",
        db_column="financial_claims_status_id", null=True, blank=True)
    issued_date = models.DateField()
    letter_status = models.ForeignKey(
        LetterStatus, related_name="letter_status_id", db_column="letter_status_id")

    class Meta:
        managed = False
        db_table = "LetterData"
        ordering = ('letter_data_id',)

    def __str__(self):
        return self.letter_title

    def __repr__(self):
        return self.letter_title


class LetterDataLogger(AbstractDateModels):
    log_id = models.AutoField(primary_key=True)
    log_message = models.CharField(max_length=2048)
    letter_data = models.ForeignKey(
        LetterData, related_name="letter_Id", db_column="letter_Id")
    user_id = models.ForeignKey(User, related_name="letter_user_id")
    from_status = models.ForeignKey(
        LetterStatus, related_name="from_status", db_column="from_status", null=True, blank=True)
    to_status = models.ForeignKey(
        LetterStatus, related_name="to_status", db_column="to_status")

    class Meta:
        managed = False
        db_table = 'LetterDataLogger'
        ordering = ('log_id',)

    def __str__(self):
        return self.log_message

    def __repr__(self):
        return self.log_message


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
