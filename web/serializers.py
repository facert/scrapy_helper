# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from web.models import Project, Rule, Field


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = "__all__"


class FieldNestedSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=True)

    class Meta:
        model = Field
        fields = "__all__"


class RuleNestedSerializer(serializers.ModelSerializer):
    # fields = FieldSerializer(many=True, required=True)
    fields = serializers.SerializerMethodField("get_fields_data")
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Rule
        fields = ("id", "path", "callback_func", "fields")

    def get_fields_data(self, obj):
        return FieldNestedSerializer(Field.objects.filter(rule=obj), many=True).data


class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule
        fields = "__all__"


class ProjectDetailSerializer(serializers.ModelSerializer):
    user_agents = serializers.CharField(required=False)
    pipelines = serializers.CharField(required=False)
    # rules = RuleNestedSerializer(many=True, required=True)
    rules = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    # user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Project
        depth = 2
        fields = ("id", "name", "alias", "domain", "start_urls", "user_agents", "pipelines", "download_delay",
                  "status", "updated", "rules", "md5")

    def get_rules(self, obj):
        return RuleNestedSerializer(Rule.objects.filter(project=obj), many=True).data

    def get_status(self, obj):
        return obj.get_status_display()

    def create(self, validated_data):
        project_data = validated_data
        rules_data = project_data.pop("rules")

        project = Project.objects.create(**project_data)
        for rule_data in rules_data:
            rule_data["project_id"] = project.id
            fields_data = rule_data.pop("fields")
            Rule.objects.filter(pk=rule_data["id"]).update(**rule_data)
            for field_data in fields_data:
                field_data["rule_id"] = rule_data["id"]
                Field.objects.filter(pk=field_data["id"]).update(**field_data)
        return project

    def update(self, instance, validated_data):
        project_data = validated_data
        rules_data = project_data.pop("rules")
        Project.objects.filter(pk=project_data["id"]).update(**project_data)

        for rule_data in rules_data:
            rule_data["project_id"] = instance.id
            fields_data = rule_data.pop("fields")
            Rule.objects.filter(pk=rule_data["id"]).update(**rule_data)
            for field_data in fields_data:
                field_data["rule_id"] = rule_data["id"]
                Field.objects.filter(pk=field_data["id"]).update(**field_data)
        return instance


class ProjectListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'alias', 'status')




