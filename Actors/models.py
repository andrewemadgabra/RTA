from HelperClasses.AbstractDateModels import AbstractDateModels
from django.db import models

# Create your models here.


class EntityCassification(AbstractDateModels):
    entity_id = models.AutoField(primary_key=True)
    entity_Ar = models.CharField(max_length=128, unique=True)
    entity_En = models.CharField(max_length=128, unique=True)

    class Meta:
        managed = False
        db_table = 'EntityCassification'

    def __str__(self):
        return self.entity_En

    def __repr__(self):
        return self.entity_En


class MainActors(AbstractDateModels):
    main_actor_id = models.AutoField(primary_key=True)
    entitycassification = models.ForeignKey(
        EntityCassification, models.CASCADE)
    main_actor_Ar = models.CharField(max_length=128, unique=True)
    main_actor_En = models.CharField(max_length=128, unique=True)

    class Meta:
        managed = False
        db_table = 'MainActors'

    def __str__(self):
        return self.main_actor_En

    def __repr__(self):
        return self.main_actor_En


class SubActors(AbstractDateModels):
    sub_actor_id = models.AutoField(primary_key=True)
    main_actor = models.ForeignKey(
        MainActors, models.CASCADE)
    sub_actor_Ar = models.CharField(max_length=128, unique=True)
    sub_actor_En = models.CharField(max_length=128, unique=True)
    sub_actor_key = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'SubActors'

    def __str__(self):
        return self.sub_actor_En

    def __repr__(self):
        return self.sub_actor_En
