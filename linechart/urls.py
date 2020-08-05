from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('simple_task', views.simple_task, name='simple_task'),
    path('graph', views.random_generator, name='graph'),
    path('fetch_test', views.fetch_test, name='fetch_test'),
    path('poll_state', views.poll_state, name='poll_state'),
    path('update_progress', views.update_progress, name='update_progress'),
    path('fetch_progress', views.fetch_progress, name='fetch_progress')

]