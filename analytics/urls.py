from django.urls import path
from .views import graph_report

urlpatterns = [
    path('admin/graph-report/', graph_report, name='graph_report'),
]
