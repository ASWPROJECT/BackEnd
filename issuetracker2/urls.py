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
from users.views import register_view, login_view, logout_view, edit_user_profile_view, change_picture_profile_view, view_profile, view_users
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Issue Tracker 2 API",
      default_version='v1',
      description="API doc for ASW project Issue Tracker 2",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

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
    path('change_picture_profile/', change_picture_profile_view, name='picture_profile'),
    path('profile/<str:username>', view_profile, name='view_profile'),
    path('list_users/', view_users, name='view_users'),

    path('swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
