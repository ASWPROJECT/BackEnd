"""issuetracker2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from issues.views import issues_view, new_issue_view, delete_by_id, view_isue, edit_issue, add_comment, bulk_insert, remove_all_activities,  add_file, delete_file, block_issue_view, desblock_issue_view, view_profile_view, download_file
from users.views import register_view, login_view, logout_view, edit_user_profile_view, change_picture_profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('issues.urls')),
    path('', issues_view, name='allIssues'),
    path('newIssues/', new_issue_view, name='getData'),
    path('delete/Issue', delete_by_id, name='getData'),
    path('issue/<int:issue_id>', view_isue, name='getData'),
    path('editIssue/', edit_issue, name='getData'),
    path('add_comment/', add_comment, name='addComment'),
    path('bulk_insert/', bulk_insert, name='bulkInsert'),
    path('delete_activities/', remove_all_activities, name='deleteActivities'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('social-auth/', include('social_django.urls'), name = 'social'),
    path('user-settings/user-profile/', edit_user_profile_view, name='edit_user_profile'),
    path('add_file/', add_file, name='addFile'),
    path('delete/file/', delete_file, name='deleteFile'),
    path('download/file/<int:id>', download_file, name='downloadFile'),
    path('issue/<int:issue_id>/block_issue/', block_issue_view, name='block_issue'),
    path('issue/<int:issue_id>/desblock_issue/', desblock_issue_view, name='desblock_issue'),
    path('view_profile/', view_profile_view, name='view_profile'),
    path('change_picture_profile/', change_picture_profile_view, name='picture_profile')
]
