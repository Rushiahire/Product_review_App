from django.urls import path
from . import views


urlpatterns = [
    path('',views.HomePage.as_view(),name='homepage'),
    path('login',views.LoginUser.as_view(),name='login_user'),
    path('logout',views.LogoutUser.as_view(),name='logout_user'),
    path('signup',views.SignupUser.as_view(),name='signupUser')
]
