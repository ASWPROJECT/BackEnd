from rest_framework import routers
from issues import api

router = routers.DefaultRouter()

router.register('api/issues', api.IssueViewSet, 'licitacions_publiques')

urlpatterns = router.urls