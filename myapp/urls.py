from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('add_post/', views.add_post, name='add_post'),
    path('chats/',views.chat_view,name='chats'),
    path('chat/<int:recipient_id>/', views.chat, name='chat'),
    path('reels/', views.reels, name='reels'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
]
