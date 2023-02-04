from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logina, name='login'),
    path('logout/', views.logouta, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>', views.userProfile, name='user-profile'),
    path('topics',views.topics, name='topics'),
    path('create_room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('del-mes/<str:pk>/', views.delmes, name='del-mes'),
    path('update-user/', views.update_user, name='update-user'),
    path('activity/', views.activity, name='activity'),
    
]