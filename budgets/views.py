from decimal import InvalidOperation, Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
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
        b.duration = request.POST.get("duration","").strip()

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

@login_required
def edit_budget(request, id):
    budget = get_object_or_404(Budget, id=id, user=request.user)
    if request.method == "POST" and request.POST['title'] != "":
        budget.title = request.POST.get("title","").strip()
        budget.description = request.POST.get("description","").strip()
        budget.category = request.POST.get("category","").strip()

        amt = request.POST.get("amount","0").strip()
        try:
            budget.amount = Decimal(amt)
        except (InvalidOperation, ValueError):
            # no change
            budget.amount = budget.amount

        budget.save()

        return redirect("Budgets.index")

    # on GET, just show the form with the existing values
    return render(request, "budgets/edit.html", {"budget": budget})

@login_required
def delete_budget(request, id):
    budget = get_object_or_404(Budget, id=id, user=request.user)
    budget.delete()
    return redirect("Budgets.index")


