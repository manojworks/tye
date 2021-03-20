from django.urls import path

from . import views

app_name = 'taxonomy'
urlpatterns = [
    path('', views.list_all, name='taxonomy_list_all'),
    path('descr/<str:product_description>/', views.list_by_descr, name='taxonomy_list_by_description'),
    path('id/<str:pk>/', views.ProductDetailsView.as_view(), name='taxonomy_list_by_id'),
    path('parent-id/<str:product_id>/', views.list_by_parent_id, name='taxonomy_list_by_parent_id'),
]