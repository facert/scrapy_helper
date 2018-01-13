# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as user_login, authenticate, logout as user_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import hashlib
import json
from rest_framework import viewsets
from rest_framework.views import Response
from web.serializers import *
from web.models import Project, Rule, Field, update_crawl_tmeplate
from web.template_engine import generate_crawl
from web.utils import create_md5


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                user_login(request, user)
            return redirect('/project')
    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if username and email and password:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            user_login(request, user)
            return redirect('/project')
    return redirect('/project')


def logout(request):
    user_logout(request)
    return redirect('/project')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


def create_view(request):
    return render(request, "project_create.html")


class ProjectViewSet(viewsets.ViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer

    def list(self, request):
        public_projects = self.queryset.filter(is_public=True, is_delete=False)
        if request.user.is_authenticated:
            personal_projects = self.queryset.filter(is_public=False, is_delete=False, user=request.user)
        else:
            personal_projects = []
        return render(request, "project_list.html", {"public_projects": public_projects, "personal_projects": personal_projects})

    def retrieve(self, request, pk=None):
        queryset = self.queryset.filter(id=pk)
        queryset = queryset[0] if queryset else None
        if not queryset:
            return JsonResponse({"msg": "project not found"})
        if queryset.is_public or queryset.user == request.user:
            serializer = ProjectDetailSerializer(queryset)
            if queryset.is_public:
                render_template = "project_public.html"
            else:
                render_template = "project_detail.html"
            return render(request, render_template, {"project": serializer.data})
        return JsonResponse({"msg": "project not found"})

    @method_decorator(login_required)
    def create(self, request):
        data = request.data.copy()
        data["user"] = request.user
        data["md5"] = create_md5()
        data["status"] = 1
        serializer = ProjectDetailSerializer(data=data)
        if serializer.is_valid():
            project = serializer.create(data)
            update_crawl_tmeplate(project)
            return Response({"msg": "ok", "id": project.id})
        return Response(serializer.errors)

    @method_decorator(login_required)
    def update(self, request, pk=None):
        queryset = self.queryset.filter(id=pk, user=request.user)
        queryset = queryset[0] if queryset else None
        if not queryset:
            return Response({"msg": "project not found"})
        data = request.data.copy()
        data["user"] = request.user
        serializer = ProjectDetailSerializer(queryset, data=data)
        if serializer.is_valid():
            instance = serializer.update(queryset, data)
            update_crawl_tmeplate(instance)
            return Response({"msg": "ok", "data": {"id": instance.id}})
        return Response(serializer.errors)

    @method_decorator(login_required)
    def destroy(self, request, pk=None):
        project = Project.objects.get(pk=pk, user=request.user)
        project.is_delete = True
        project.save()
        return Response({"msg": "ok"})


def project_status(request, id):
    if request.method == 'GET':
        project = get_object_or_404(Project, pk=id)
        if project.is_public or project.user == request.user:
            return render(request, "project_status.html", {"project": project})
    if request.method == "POST":
        user = request.user
        body = json.loads(request.body)
        id = body.get("id")
        status = int(body.get("status", 0))
        project = Project.objects.get(pk=id, user=user)
        project.status = status
        project.save()

        rule_fields = []
        rules = Rule.objects.filter(project=project)
        for rule in rules:
            fields = Field.objects.filter(rule=rule)
            rule_fields.append({"rule": rule, "fields": fields})

        if status == 1:
            generate_crawl(project, rule_fields)
        return JsonResponse({"msg": "ok"})
    return JsonResponse({"msg": "method not allowed"})


class RuleViewSet(viewsets.ModelViewSet):

    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

    def create(self, request):
        serializer = RuleSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"msg": "ok", "data": {"id": instance.id}})
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        Rule.objects.filter(pk=pk).delete()
        return Response({"msg": "ok"})


class FieldViewSet(viewsets.ModelViewSet):

    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def create(self, request):
        serializer = FieldSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response({"msg": "ok", "data": {"id": instance.id}})
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        Field.objects.filter(pk=pk).delete()
        return Response({"msg": "ok"})