from django.urls import path
from .views import *

urlpatterns = [
    path('blog/',BlogApiView.as_view(),name='blog'),
    path('blog/<int:pk>/',BlogIdApiView.as_view(),name='blog detail'),
    # path('user-info/',UserInfo.as_view(),name='user info detail'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('admin-create/',admin_create,name='admin-create'),
    path('group/',GroupApiView.as_view(),name='group list'),
    path('category/',CategoryApiView.as_view(),name='Category list'),
    path('category/<int:pk>/',CategoryIdApiView.as_view(),name='Category list detail'),
]