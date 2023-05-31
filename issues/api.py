from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from issues.models import *
from users.models import *
from issues.serializers import *
from users.serializers import *
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
    
    def delete(self, request):
        try:
            Issue.objects.all().delete()
        except Issue.DoesNotExist:
            return Response({'error': 'No hay Issues'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_202_ACCEPTED)

class ViewIssue(APIView):
    def get(self, request, pk):
        try:
            issue = Issue.objects.get(pk=pk)
        except Issue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = IssueDetailSerializer(issue)
        users = User.objects.all()
        user_serializer = UserPreviewSerializer(users, many=True)
        response_data = serializer.data
        response_data['users'] = user_serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

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


class AssignUser(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request, pk):
        creator = request.user
        user = request.data.get("user")
        user_db = get_object_or_404(User, id=user)
        issue = get_object_or_404(Issue, pk=pk)
        old_user = None
        try:
            old_assigned_user = AsignedUser.objects.get(Issue=issue)
            old_user = old_assigned_user.User
        except AsignedUser.DoesNotExist:
            pass
        AsignedUser.objects.filter(Issue=issue).delete()
        AsignedUser.objects.create(
            Issue=issue,
            User=user_db)
        Activity.objects.create(
            Creator = creator,
            Issue = issue,
            Type = 'assigned to',
            Old_user = old_user,
            User = user_db
        )
        return Response(status=status.HTTP_201_CREATED)
    

class AssignUserClear(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request, pk):
        creator = request.user
        issue = get_object_or_404(Issue, pk=pk)
        old_user = None
        try:
            old_assigned_user = AsignedUser.objects.get(Issue=issue)
            old_user = old_assigned_user.User
        except AsignedUser.DoesNotExist:
            pass
        AsignedUser.objects.filter(Issue=issue).delete()
        Activity.objects.create(
            Creator = creator,
            Issue = issue,
            Type = 'assigned to',
            Old_user = old_user,
            User = None
        )
        return Response(status=status.HTTP_200_OK)
    

class WatchUser(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        try:
            users = request.data.get("users")
            print(users)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Watcher.objects.filter(Issue=issue).delete()
        for user in users:
            user_db = get_object_or_404(User, id=user)
            try:
                Watcher.objects.create(
                    User=user_db,
                    Issue=issue
                )
            except IntegrityError:
                # Handle the case when a Watcher with the same user and issue already exists
                pass
        return Response(status=status.HTTP_201_CREATED)


class WatchUserClear(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request, pk):
        issue = get_object_or_404(Issue, pk=pk)
        user = request.data.get("user")
        user_db = get_object_or_404(User, id=user)
        Watcher.objects.filter(Issue=issue, User=user_db).delete()
        return Response(status=status.HTTP_200_OK)
    

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
        serializer = IssueDetailSerializer(issue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class AddFiles(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def post(self, request):
        file = request.FILES.get('file')
        issue_id = request.POST.get('issue_id')
        issue = get_object_or_404(Issue, id = issue_id)

        AttachedFile.objects.create(
            Issue = issue,
            File = file,
            Name = str(file)
        )
        serializer = IssueDetailSerializer(issue)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class Files(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)
    
    def get(self, request, id):
        try:
            file = AttachedFile.objects.get(id = id)
            serializer = AttachedFileSerializer(file)
        except AttachedFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        try:
            AttachedFile.objects.get(id = id).delete()
        except AttachedFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_202_ACCEPTED)
    
class ToggleBlockIssue(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)


    def put(self, request, issue_id):
        issue = get_object_or_404(Issue, id=issue_id)
              
        issue.Block_reason = request.POST.get('block_reason')
        issue.save()
        serializer = IssueSerializer(issue, data=request.data)        
        
        if request.POST.get('block_reason') != None:
            try:
                Activity.objects.create(
                    Creator = User.objects.get(username=request.user.username),
                    Issue = issue,
                    Type = "Blocked"
                )
            except:
                return Response({'error': 'Al crear el activity'}, status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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

class Activities(APIView):
    authentication_classes(IsAuthenticated,)
    permission_classes(TokenAuthentication,)

    def get(self, request):
        try:
            queryset = Activity.objects.filter(Q(User = request.user)|Q(Creator = request.user))
            return Response (ActivitySerializer(queryset, many = True).data, status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            return Response({'error': 'No hay Activities'}, status=status.HTTP_404_NOT_FOUND)
