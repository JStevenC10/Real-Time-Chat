from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("info/", views.InfoView.as_view(), name="info"),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name='login.html'), name='login'),
    path("<str:username>/profile/", views.view_profile, name="profile"),
    path("logout/", views.logout_user, name='logout'),
    path('chat/<str:room_name>/', views.chatroom, name='chatroom'),
    path('create/room/', views.new_room, name='new_chat'),
    path('delete/chat/room/<int:pk>/', views.delete_room, name='delete_room'),
]
