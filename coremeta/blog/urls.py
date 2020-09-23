from django.urls import path, include
from django.contrib.auth import views

from django.conf.urls import include, url
from . import views
from . import views as core_views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('content/<slug:slug>/', views.post_detail, name='post_detail'),
]