from django.urls import path

from . import views

urlpatterns = [
    path('', views.list_all, name='taxonomy_list_all'),
]