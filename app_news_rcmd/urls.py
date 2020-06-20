from django.urls import path
from app_news_rcmd import views

app_name="namespace_app_news_rcmd"

urlpatterns = [
    path('', views.home, name = "home"),
    path('api_keywords_similar_news/', views.api_keywords_similar_news),
    path( "api_cate_news/", views. api_cate_news),
    path( "api_news_content/", views. api_news_content),
]