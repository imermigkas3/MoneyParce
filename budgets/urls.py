from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='Budgets.index'),
    path('create/', views.create_budget, name='Budgets.create_budget'),
]