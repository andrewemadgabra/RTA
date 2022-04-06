from django.db import models
from HelperClasses.AbstractDateModels import AbstractDateModels
from HelperClasses.DjangoValidator import DjangoValidator


class MainTopic(AbstractDateModels):
    main_topic_id = models.AutoField(primary_key=True)
    main_topic_Ar = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    main_topic_En = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'MainTopic'

    def __str__(self):
        return self.main_topic_En

    def __repr__(self):
        return self.main_topic_En


class TopicClassification(AbstractDateModels):
    topic_classification_id = models.AutoField(primary_key=True)
    topic_classification_Ar = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    topic_classification_En = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])
    main_topic = models.ForeignKey(
        MainTopic, models.CASCADE, related_name="main_topic_classification", db_column="main_topic_id")

    class Meta:
        managed = False
        db_table = 'TopicClassification'

    def __str__(self):
        return self.topic_classification_En

    def __repr__(self):
        return self.topic_classification_En


class TopicSubcategories(AbstractDateModels):
    topic_subcategories_id = models.AutoField(primary_key=True)
    topic_subcategories_Ar = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    topic_subcategories_En = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])
    topic_classification = models.ForeignKey(
        TopicClassification, models.CASCADE, related_name="topic_class_subcat", db_column="topic_classification_id")

    class Meta:
        managed = False
        db_table = 'TopicSubcategories'

    def __str__(self):
        return self.topic_subcategories_En

    def __repr__(self):
        return self.topic_subcategories_En
