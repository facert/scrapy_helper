# coding: utf-8

from django.conf.urls import include, url

from web import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'rule', views.RuleViewSet)
router.register(r'field', views.FieldViewSet)


urlpatterns = [
    url(r'^accounts/login', views.login),
    url(r'^accounts/register', views.register),
    url(r'^accounts/logout', views.logout),
    url(r'^project/create', views.create_view),
    url(r'^project_status/(?P<id>\d+)$', views.project_status),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]