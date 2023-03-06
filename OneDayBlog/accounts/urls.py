from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = 'profile'
urlpatterns = [
    path('follow/<int:id>/',views.FollowCreateApiView.as_view(),name='follow'),
    path('unfollow/<int:id>/',views.UnFollowApiView.as_view(),name='unfollow'),
    path('dashboard/<int:id>/',views.DashboardApiView.as_view(),name='dashboard'),
    path('login/',views.LoginApiView.as_view(),name='login'),
    path('logout/',views.LogoutApiView.as_view(),name='logout'),
    path('register/',views.RegisterApiView.as_view(),name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]