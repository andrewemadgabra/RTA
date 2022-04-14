from HelperClasses.AbstractDateModels import AbstractDateModels
from django.db import models
from HelperClasses.DjangoValidator import DjangoValidator

# Create your models here.


class EntityCassification(AbstractDateModels):
    entity_id = models.AutoField(primary_key=True)
    entity_Ar = models.CharField(max_length=128, unique=True,  validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    entity_En = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'EntityCassification'
        ordering = ('entity_id',)

    def __str__(self):
        return self.entity_En

    def __repr__(self):
        return self.entity_En


class MainActors(AbstractDateModels):
    main_actor_id = models.AutoField(primary_key=True)
    entitycassification = models.ForeignKey(
        EntityCassification, models.CASCADE)
    main_actor_Ar = models.CharField(max_length=128, unique=True,  validators=[
        DjangoValidator().validation_ArabicLettersOrNumbers])
    main_actor_En = models.CharField(max_length=128, unique=True, validators=[
        DjangoValidator().validation_EnglishLetters])

    class Meta:
        managed = False
        db_table = 'MainActors'
        ordering = ('main_actor_id',)

    def __str__(self):
        return self.main_actor_En

    def __repr__(self):
        return self.main_actor_En


class SubActors(AbstractDateModels):
    sub_actor_id = models.AutoField(primary_key=True)
    main_actor = models.ForeignKey(
        MainActors, models.CASCADE)
    sub_actor_Ar = models.CharField(max_length=128, unique=True, validators=[
                                    DjangoValidator().validation_ArabicLettersOrNumbers])
    sub_actor_En = models.CharField(max_length=128, unique=True, validators=[
                                    DjangoValidator().validation_EnglishLetters])
    sub_actor_parent = models.ForeignKey(
        "self",  models.CASCADE, db_column='sub_actor_parent', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SubActors'
        ordering = ('sub_actor_id',)

    def __str__(self):
        return self.sub_actor_En

    def __repr__(self):
        return self.sub_actor_En
