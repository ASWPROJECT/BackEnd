from rest_framework import routers
from issues import api
from django.urls import path, include
from .views import lista_issues



router = routers.DefaultRouter()

router.register('api/issues', api.IssueViewSet, 'licitacions_publiques')


urlpatterns = [
    #router.urls,
    path('/issuetracker2/frontend/issues.html/', lista_issues, name='lista_issues'),
 
]