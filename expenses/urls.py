from django.urls import path

from . import views

app_name = 'expenses'
urlpatterns = [
    path('new-expense', views.new_expense, name='new_expense'),
    path('new-expense/get/ajax/validate/filterproducts', views.filter_products, name='filter_products'),
    path('recent-expenses', views.recent_expenses, name='recent_expenses'),
]
