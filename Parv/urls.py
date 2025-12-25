
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , views.register, name="register"),
    path('login' , views.Login_view , name="login"),
    path('logout/', views.Logout, name='Logout'),
    path('home', views.home , name="home"),
    path('track', views.track , name="track"),
]
