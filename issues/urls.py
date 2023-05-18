from issues import api
from django.urls import path


urlpatterns = [
    path('issues', api.IssuesView.as_view()),
    path('issues/<int:pk>', api.ViewIssue.as_view()),
    path('issues/<int:pk>/comments', api.AddComment.as_view()),
    path('issues/bulk-insert', api.BulkInsert.as_view()),
    path('comments', api.CommentsView.as_view()),
    path('files', api.FilesView.as_view())    
]