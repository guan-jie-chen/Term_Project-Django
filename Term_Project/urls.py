"""Term_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include

urlpatterns = [
    #path('admin/', admin.site.urls),

    #path('topword/', include('app_top_keyword.urls')),
    path('', include('app_top_keyword.urls')),  # default home

    # app top persons
    path('topperson/', include('app_top_person.urls')),

    # app top ner analysis
    path('topner/', include('app_top_ner_analysis.urls')),

    # app user keyword
    path('userkeyword/', include('app_user_keyword.urls')),

    # news recommendation
    path('news_rcmd/', include('app_news_rcmd.urls')),

    # Sentiment analysis
    path('sentiment/', include('app_sentiment.urls')),

    # news classification
    path('news_cate/', include('app_news_classify.urls')),



]
