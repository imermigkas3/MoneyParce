from decimal import InvalidOperation, Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
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

@login_required
def create_budget(request):
    if request.method == "POST" and request.POST['title'] != "":
        b = Budget()
        b.user = request.user
        b.title = request.POST.get("title","").strip()
        b.description = request.POST.get("description","").strip()
        b.category = request.POST.get("category","").strip()

        amt = request.POST.get("amount","0").strip()

        try:
            b.amount = Decimal(amt)
        except (InvalidOperation, ValueError):
            b.amount = Decimal("0")
        b.save()

        return redirect("/budgets/")

    # if GET or missing title, just show the form again
    return render(request,
                  "budgets/create.html")



