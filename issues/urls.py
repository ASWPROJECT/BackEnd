from issues import api
from django.urls import path


urlpatterns = [
    path('', api.IssuesView.as_view()),
    path('<int:pk>', api.ViewIssue.as_view()),
    path('<int:pk>/comments', api.AddComment.as_view()),
    path('<int:issue_id>/toggle_block_issue/', api.ToggleBlockIssue.as_view()),
    path('<int:id>/delete', api.DeleteIssues.as_view()), 
    path('bulk-insert', api.BulkInsert.as_view()),
    path('files/', api.AddFiles.as_view()),
    path('files/<int:id>', api.Files.as_view()),
    path('activities', api.Activities.as_view()),
]