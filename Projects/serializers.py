from rest_framework import serializers
from Projects.models import Projects, ProjectSections, ProjectContracts


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = "__all__"
        read_only_fields = ('project_id', 'created_at')


class ProjectSectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectSections
        fields = "__all__"
        read_only_fields = ('project_section_id', 'created_at')


class ProjectContractsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectContracts
        fields = "__all__"
        read_only_fields = ('project_contract_id', 'created_at')


class ProjectSectionsGETSerializer(serializers.ModelSerializer):
    project = ProjectsSerializer()

    class Meta:
        model = ProjectSections
        fields = "__all__"
        read_only_fields = ('project_section_id', 'created_at')


class ProjectContractsGETSerializer(serializers.ModelSerializer):
    project_section = ProjectSectionsSerializer()

    class Meta:
        model = ProjectContracts
        fields = "__all__"
        read_only_fields = ('project_contract_id', 'created_at')

