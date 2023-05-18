from django.shortcuts import get_object_or_404
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
            try:
                queryset = Issue.objects.all().order_by(order_by)
            except Issue.DoesNotExist:
                return Response({'error': 'No hay Issues'}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:
                queryset = Issue.objects.all()
            except Issue.DoesNotExist:
                return Response({'error': 'No hay Issues'}, status=status.HTTP_404_NOT_FOUND)

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


class ViewIssue(APIView):

    def get(self, request, pk):
        try:
            issue = Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IssueDetailSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            issue = Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = IssueDetailSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
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
        try:
            subjects = request.data.get('subjects')
            print(subjects)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for subject in subjects:
            Issue.objects.create(
                Subject=subject,
                Creator=user
            )
        return Response(status=status.HTTP_201_CREATED)


class AddComment(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request, pk):
        user = request.user
        comment = request.data.get('comment')
        issue = get_object_or_404(Issue, pk=pk)
        Comment.objects.create(
            Comment=comment,
            Issue=issue,
            Creator=user)
        return Response(status=status.HTTP_201_CREATED)
    
class Files(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request, pk):
        file = request.FILES.get('File')
        issue_id = request.POST.get('issue_id')
        issue = get_object_or_404(Issue, id = issue_id)

        AttachedFile.objects.create(
            Issue = issue,
            File = file,
            Name = str(file)
        )
        return Response(status=status.HTTP_201_CREATED)
    
    def get(self, pk):
        try:
            file = AttachedFile.objects.get(pk = pk)
            serializer = AttachedFileSerializer(file)
        except AttachedFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        try:
            AttachedFile.objects.delete(pk = pk)
        except AttachedFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)
    
class ToggleBlockIssue(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)


    def put(self, request, pk):
        issue_id = request.PUT.get('issue_id')
        issue = get_object_or_404(Issue, id=issue_id)
              
        issue.Block_reason = request.PUT.get('block_reason')
        issue.save()
        serializer = IssueSerializer(issue)
        serializer.save()
        
        
        if request.PUT.get('block_reason') != None:
            try:
                Activity.objects.create(
                    creator = User.objects.get(username=request.user.username),
                    issue = issue,
                    type = "Blocked"
                )
            except:
                return Response({'error': 'Al crear el activity'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteIssues(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def delete(self, request, id):
        if request.method == 'DELETE':
            try:
                Issue.objects.filter(id=id).delete()
            except Issue.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_200_OK)

