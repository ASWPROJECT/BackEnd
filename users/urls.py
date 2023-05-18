from users import api
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('register/', api.RegisterView.as_view()),
    path('login/', api.LoginView.as_view()),
    path('logout/', api.Logout.as_view()),
    path('user-settings/user-profile/', api.EditProfileView.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  



]