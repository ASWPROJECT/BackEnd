from issues import models, serializers
from rest_framework import viewsets, permissions


class IssueViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.IssueSerializer