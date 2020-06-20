from django.urls import path 
from app_top_person import views

app_name = 'app_top_person'

urlpatterns = [  
    
    # top (popular) persons
    path('', views.chart_topPerson, name='home_topPerson'),
    # ajax path
    path('api_get_topPerson/', views.api_get_topPerson, name='api_get_topPerson'),
]
