from issues import api
from django.urls import path


urlpatterns = [
    path('issues', api.IssuesView.as_view()),
    path('comments', api.CommentsView.as_view()),
    path('files', api.FilesView.as_view())
]