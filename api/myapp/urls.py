from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('register',views.register, name='register'),
    path('start', views.start, name='start'),       
    path('init', views.init, name='init')
]
