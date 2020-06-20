from django.urls import path
from app_top_keyword import views

# declare a  namespace for this APP
# the name of namespace is  'app_top_keyword'
# We will use the namespace in the future integrated website.
app_name = 'app_top_keyword'

urlpatterns = [
    # top keywords
    path('', views.chart_cate_topWord, name='chart_topWord'),
    path('api_get_cate_topWord', views.api_get_cate_topWord, name='api_cate_topWord'),
]
