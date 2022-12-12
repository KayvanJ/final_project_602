from django.urls import path

from . import views

urlpatterns = [
    path('', views.loading, name='loading'),
    path('home/', views.home, name='home'),
]
