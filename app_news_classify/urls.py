from django.contrib import admin
from django.urls import path
from app_news_classify import views

app_name='namespace_app_news_classify'

urlpatterns = [
    path('', views.home, name='home'),
    path('api_get_news_cate/', views.api_get_news_cate, name='api_get_news_cate'),
]
