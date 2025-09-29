from django.urls import path
from . import views as views

app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('session/', views.session_view, name='session'),
    path('register/', views.register_view, name='register'),
]