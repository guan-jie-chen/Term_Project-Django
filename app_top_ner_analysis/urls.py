from django.urls import path
from app_top_ner_analysis import views

app_name="namespace_top_ner"

urlpatterns = [
    path('', views.home, name='home'),
    path('api_get_cate_topkey/', views.api_get_cate_topkey, name='api_cate_topkey'),
]