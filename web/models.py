# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from web.template_engine import generate_crawl


class Project(models.Model):

    PIPELINE_CHOICES = {
        "1": "JsonWriterPipeline",
        "2": "ImagesPipeline",
        "3": "MongoPipeline",
        "4": "CsvWriterPipeline",
        "5": "ElasticSearchPipeline"
    }

    RUN_STATUS = (
        (0, u"构建中"),
        (1, u'初始化'),
        (2, u'运行'),
        (3, u'停止'),
    )

    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    alias = models.CharField(max_length=200)
    domain = models.TextField()
    start_urls = models.TextField()
    user_agents = models.TextField(default="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0")
    pipelines = models.CharField(max_length=100)
    download_delay = models.IntegerField(default=3)

    image_urls = models.CharField(max_length=50, null=True, blank=True)
    images = models.CharField(max_length=50, null=True, blank=True)

    md5 = models.CharField(max_length=64, null=True, blank=True)
    status = models.IntegerField(choices=RUN_STATUS, default=0)

    is_public = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def get_pipelines(self):
        return [self.PIPELINE_CHOICES[pipeline] for pipeline in self.pipelines.split(",")]


class Rule(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True)
    path = models.CharField(max_length=256)
    callback_func = models.CharField(max_length=50, verbose_name=u"回调", null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Field(models.Model):
    rule = models.ForeignKey(Rule, null=True, blank=True)
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


def update_crawl_tmeplate(project):
    rule_fields = []
    rules = Rule.objects.filter(project=project)
    for rule in rules:
        fields = Field.objects.filter(rule=rule)
        rule_fields.append({"rule": rule, "fields": fields})

    generate_crawl(project, rule_fields)
