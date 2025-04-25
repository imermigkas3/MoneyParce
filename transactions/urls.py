from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),

    path('fetch-bank-transactions/', views.fetch_bank_transactions, name='fetch_bank_transactions'),


    path('report-data/', views.user_report_data, name='user-report-data'),

    # Updated line below:
    path('report/', views.report_view, name='user-report-page'),
    path('send-email/', views.send_email, name="send-email"),
]

