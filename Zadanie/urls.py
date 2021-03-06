"""Zadanie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from Zadanie_app.views import FileListView, FileDetailView, FileCreateView, FileDeleteView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('files/', FileListView.as_view(), name='files_list'),
    path('<int:pk>/file/update/<slug>/', FileDetailView.as_view(), name='file_detail'),
    path('<int:pk>/file/delete/', FileDeleteView.as_view(), name='file_delete'),
    path('file/create/', FileCreateView.as_view(), name='file_create'),
]
