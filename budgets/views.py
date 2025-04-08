from django.shortcuts import render
from .models import Budget

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Budgets'
    #Expense.objects manager in Django that serves as the default interface to query the database table associated with the model.
    #more info on page 155
    #provides various methods to perform database operations such as creating, updating, deleting, and retrieving objects.
    template_data['Budgets'] = Budget.objects.all()
    return render(request, 'budgets/index.html',
                  {'template_data' : template_data})