# chat/urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('base/', views.base, name='base'),
    path('chat/<str:room_name>/<str:username>/', views.chat, name='chat'),
    path('', views.create_room, name='create_room'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', views.login, name='login'),
    path('singup/', views.signup, name='signup'),
    path('main/', views.main, name='main'),
]