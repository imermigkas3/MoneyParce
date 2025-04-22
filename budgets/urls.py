from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='Budgets.index'),
    path('create/', views.create_budget, name='Budgets.create_budget'),
    path('<int:id>/edit/',views.edit_budget, name='Budgets.edit_budget'),
    # when the browser requests /budgets/123/delete/ for exampple,
    # call views.delete_budget(request, id=123)
    path('<int:id>/delete/', views.delete_budget, name="Budgets.delete_budget")
]