from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from User.models import User
from HelperClasses.DjangoValidator import DjangoValidator
from django.conf import settings
import os
# Create your models here.


class LetterData(AbstractDateModels):
    letter_data_id = models.AutoField(primary_key=True)
    issued_number = models.PositiveIntegerField()
    letter_title = models.CharField(max_length=256)
    action_user = models.ForeignKey(
        User, models.CASCADE, related_name="creator_letter", db_column="action_user")

    class Meta:
        managed = False
        db_table = "LetterData"

    def __str__(self):
        return self.letter_title

    def __repr__(self):
        return self.letter_title


class AttachmentType(AbstractDateModels):
    attachment_type_id = models.AutoField(primary_key=True)
    attachment_type_ar = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    attachment_type_en = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])

    content_type = models.CharField(max_length=128)
    charset = models.CharField(max_length=128, null=True, blank=True)
    max_size = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'AttachmentType'

    def __str__(self):
        return self.attachment_type_en

    def __repr__(self):
        return self.attachment_type_en


class LetterAttachments(AbstractDateModels):
    letter_attachment_id = models.AutoField(primary_key=True)
    letter_data = models.ForeignKey(LetterData, models.CASCADE)
    letter_attach_name = models.CharField(max_length=128)
    file_path_on_server = models.FilePathField(path=os.path.join(
        settings.BASE_DIR, settings.JSON_CONFIGRATION['STATIC_DIR']))
    attachment_type = models.ForeignKey(AttachmentType, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'LetterAttachemnets'

    def __str__(self):
        return self.letter_attach_name

    def __repr__(self):
        return self.letter_attach_name
