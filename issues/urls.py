from issues import api
from django.urls import path


urlpatterns = [
    path('', api.IssuesView.as_view()),
    path('<int:pk>', api.ViewIssue.as_view()),
    path('<int:pk>/comments', api.AddComment.as_view()),
    path('<int:pk>/assign', api.AssignUser.as_view()),
    path('<int:pk>/watch', api.WatchUser.as_view()),
    path('<int:pk>/assign/clear', api.AssignUserClear.as_view()),
    path('<int:pk>/watch/clear', api.WatchUserClear.as_view()),
    path('<int:issue_id>/toggle_block_issue/', api.ToggleBlockIssue.as_view()),
    path('<int:id>/delete', api.DeleteIssues.as_view()), 
    path('bulk-insert', api.BulkInsert.as_view()),
    path('files/', api.AddFiles.as_view()),
    path('files/<int:id>', api.Files.as_view()),
    path('activities', api.Activities.as_view()),
]