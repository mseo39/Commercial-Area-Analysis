from django.urls import path
from main import views
 
urlpatterns = [ 
    path('api/upload_file', views.upload_file),
    path('api/get_trdar_cd', views.get_commercial_data, name='get_trdar_cd'),
]