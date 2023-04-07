from issues import models, serializers
from rest_framework import generics
from rest_framework import viewsets, permissions
from django.db.models import Q


class IssueViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.IssueSerializer

class IssuesView(generics.ListCreateAPIView):
    serializer_class = serializers.IssueSerializer

    def get_queryset(self):
        queryset = models.Issue.objects.all()

        q = self.request.query_params.get('q')
        if q is not None:
            queryset = queryset.filter(Q(Subject__icontains=q) | Q(Description__icontains=q))
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.CommentSerializer

class CommentsView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        queryset = models.Comment.objects.all()
        return queryset