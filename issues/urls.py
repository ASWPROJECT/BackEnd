from rest_framework import routers
from issues import api
from django.urls import path, include
from . import views



router = routers.DefaultRouter()

router.register('issues', api.IssueViewSet, 'licitacions_publiques')


urlpatterns =    router.urls