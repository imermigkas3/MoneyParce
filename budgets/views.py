from decimal import InvalidOperation, Decimal

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Budget
from .services import get_budget_warnings

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Budgets'
    #Expense.objects manager in Django that serves as the default interface to query the database table associated with the model.
    #more info on page 155
    #provides various methods to perform database operations such as creating, updating, deleting, and retrieving objects.
    template_data['Budgets'] = Budget.objects.filter(user=request.user)

    budget_warning = get_budget_warnings(request.user)
    return render(request, 'budgets/index.html',
                  {'template_data' : template_data,
                        'budget_warning' : budget_warning})

@login_required
def create_budget(request):
    form_error = None
    if request.method == "POST":
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
            form_error = "You need to have a title and an amount"
            b.amount = Decimal("0")
        if b.title != "" and b.amount > 0:
            exists = Budget.objects.filter(
                user=request.user,
                category=b.category,
            ).exists()

            if exists:
                form_error = f"You already have a budget for this category: {b.category}"
            else:
                b.save()
                return redirect("Budgets.index")

    # if GET or missing title, just show the form again
    return render(request,
                  "budgets/create.html", {"form_error": form_error,
                                                                "initial": request.POST})

@login_required
def edit_budget(request, id):
    budget = get_object_or_404(Budget, id=id, user=request.user)
    form_error = None
    if request.method == "POST" and request.POST['title'] != "" and request.POST['amount'] != "0":
        budget.title = request.POST.get("title","").strip()
        budget.description = request.POST.get("description","").strip()
        budget.category = request.POST.get("category","").strip()

        amt = request.POST.get("amount","0").strip()
        try:
            budget.amount = Decimal(amt)
            budget.full_clean()  # ← runs MinValueValidator
            budget.save()
            return redirect("Budgets.index")
        except (InvalidOperation, ValueError):
            form_error = "Please enter a valid number."
        except ValidationError as e:
            form_error = e.message_dict.get('amount', ["Invalid amount"])[0]

    elif request.method == "POST":
        form_error = "You need to have a title and an amount"


    # on GET, just show the form with the existing values
    return render(request, "budgets/edit.html", {"budget": budget,
                                                                    'form_error' :form_error})

@login_required
def delete_budget(request, id):
    budget = get_object_or_404(Budget, id=id, user=request.user)
    budget.delete()
    return redirect("Budgets.index")


