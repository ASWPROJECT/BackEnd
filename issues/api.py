from issues import models, serializers
from rest_framework import generics
from django.db.models import Q


class IssuesView(generics.ListCreateAPIView):
    serializer_class = serializers.IssueSerializer

    def get_queryset(self):
        queryset = models.Issue.objects.all()

        q = self.request.query_params.get('q')
        if q is not None:
            queryset = queryset.filter(Q(Subject__icontains=q) | Q(Description__icontains=q))
        
        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(Status__icontains=status)
        
        priority = self.request.query_params.get('priority')
        if priority is not None:
            queryset = queryset.filter(Priority__icontains=priority)
        
        creator = self.request.query_params.get('creator')
        if creator is not None:
            queryset = queryset.filter(Creator__username__icontains=creator)
        return queryset


class CommentsView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        queryset = models.Comment.objects.all().order_by('-Created_at')

        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(Issue_id=id)
        return queryset
    
class FilesView(generics.ListCreateAPIView):
    serializer_class = serializers.FileSerializer

    def get_queryset(self):
        queryset = models.AttachedFile.objects.all()

        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(Issue_id=id)
        return queryset