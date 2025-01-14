# urls.py

from . import views
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views as auth_views
from .views import SignUpView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
     path('', views.root_view, name='root_view'),
    path("users/signup/", csrf_exempt(SignUpView.as_view()), name="signup"),
     path('users/token/generate/', 
          jwt_views.TokenObtainPairView.as_view(), 
          name ='token_obtain_pair'),
     path('users/token/refresh/', 
          jwt_views.TokenRefreshView.as_view(), 
          name ='token_refresh'),
     path('users/logout/', views.LogoutView.as_view(), name ='logout'),
]
