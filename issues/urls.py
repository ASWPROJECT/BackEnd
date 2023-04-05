from rest_framework import routers
from issues import api
from django.urls import path, include
from . import views



router = routers.DefaultRouter()

router.register('issues', api.IssueViewSet, 'issues')
router.register('comments', api.CommentViewSet, 'comments')


urlpatterns =    router.urls