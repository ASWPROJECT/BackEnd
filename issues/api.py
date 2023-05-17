from rest_framework.response import Response
from rest_framework import status
from issues.models import *
from issues.serializers import *
from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class IssuesView(generics.ListCreateAPIView):
    serializer_class = IssueSerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by')
        if order_by is not None:
            queryset = Issue.objects.all().order_by(order_by)
        else:
            queryset = Issue.objects.all()

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
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-Created_at')

        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(Issue_id=id)
        return queryset
    
class FilesView(generics.ListCreateAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        queryset = AttachedFile.objects.all()

        id = self.request.query_params.get('id')
        if id is not None:
            queryset = queryset.filter(Issue_id=id)
        return queryset


class BulkInsert(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request):
        user = request.user
        subjects = request.data.get('subjects', '').splitlines()
        for subject in subjects:
            Issue.objects.create(
                Subject=subject,
                Creator=user
            )
        return Response(status=status.HTTP_201_CREATED)