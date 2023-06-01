from users import api
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', api.RegisterView.as_view()),
    path('change-bio-profile/', api.EditProfileView.as_view()),
    path('profile/', api.ViewProfile.as_view()),
    path('users/', api.ViewUsers.as_view()),
    path('api-token-auth/', obtain_auth_token),  
    path('change-picture-profile/', api.ChangePictureProfileView.as_view()),  
    path('edit-user-profile/', api.UserProfileView.as_view()),  
    path('id/', api.ViewUserProfile.as_view()),  


]