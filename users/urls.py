from users import api
from django.urls import path


urlpatterns = [
    path('register/', api.RegisterView.as_view()),
    path('login/', api.LoginView.as_view()),
]