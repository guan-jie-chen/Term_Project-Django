from django.urls import path
from app_sentiment import views

app_name='namespace_app_sentiment'

urlpatterns = [
    path('', views.home, name='home'),
    path('api_get_sentiment/', views.api_get_sentiment, name='api_get_sentiment'),
]