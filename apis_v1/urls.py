from django.urls import path
from rest_framework.authtoken import views
from apis_v1 import apis 

urlpatterns = [
    path('login/', views.obtain_auth_token, name='login'),
    path('users/', apis.Users.as_view(), name='user_list'),
    path('message/<int:user_id>/', apis.Messages.as_view(), name='messages'),
]