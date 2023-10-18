"""my_front URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.main, name="main"),
    path('get_trdar_cd/', views.get_trdar_cd, name='get_trdar_cd'),
    path('data_upload',views.data_upload, name="data_upload"),
    path('data_result',views.data_result, name="data_result"),
    path('data_process',views.data_process, name="data_process"),
    path('upload_file',views.upload_file, name="upload_file"),
]
