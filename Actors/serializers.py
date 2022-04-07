from rest_framework import serializers
from Actors.models import EntityCassification, MainActors, SubActors


class EntityCassificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntityCassification
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class MainActorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainActors
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class MainActorsGETSerializer(serializers.ModelSerializer):
    entitycassification = EntityCassificationSerializer()

    class Meta:
        model = MainActors
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class SubActorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubActors
        fields = "__all__"
        read_only_fields = ('id', 'created_at')


class SubActorsGETSerializer(serializers.ModelSerializer):
    main_actor = MainActorsGETSerializer()
    count_of_children = serializers.SerializerMethodField()

    class Meta:
        model = SubActors
        fields = "__all__"
        read_only_fields = ('id', 'created_at')

    def get_count_of_children(self, obj):
        return SubActors.objects.filter(sub_actor_parent=obj.sub_actor_id).count()
