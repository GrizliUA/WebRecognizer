"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from recognizer import views

urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),
    path('control_feed/<str:action>/', views.control_feed, name='control_feed'),
    path('get_identified_items/', views.get_identified_items, name='get_identified_items'),
    path('', views.home, name='home'),
]
