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
from issues.views import file, issues_view, new_issue_view, delete_by_id, toggle_block_issue, view_isue, edit_issue, add_comment, bulk_insert, remove_all_activities, view_profile_view
from users.views import register_view, login_view, logout_view, edit_user_profile_view, change_picture_profile_view, view_profile, view_users
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('issues.urls')),
    path('users/', include('users.urls')),
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
    path('add_file/', file, name='addFile'),
    path('delete/file/', file, name='deleteFile'),
    path('download/file/<int:id>', file, name='downloadFile'),
    path('issue/<int:issue_id>/toggle_block_issue/', toggle_block_issue, name='block_issue'),
    path('view_profile/', view_profile_view, name='view_profile'),
    path('change_picture_profile/', change_picture_profile_view, name='picture_profile'),
    path('profile/<str:username>', view_profile, name='view_profile'),
    path('list_users/', view_users, name='view_users'),    
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
]
