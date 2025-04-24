from decimal import Decimal

from django.db.models import Sum

from budgets.models import Budget
from transactions.models import Transaction
import logging
logger = logging.getLogger(__name__)


def get_budget_warnings(user):
    budgets = Budget.objects.filter(user=user).exclude(category='', duration='')
    warning_categories = []

    for budget in budgets:
        logger.debug(f"category={budget.category}, display={budget.get_category_display()}")

        category = budget.category
        total =  Transaction.objects.filter(user=user,
                                            category=category).aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')

        if total >= budget.amount:
            warning_categories.append(f"{budget.get_category_display()} (Exceeded)")

        elif total >= Decimal("0.9") * budget.amount: # can't do just 0.9 because can't mix floats and Decimal (budget.amount is of type Decimal)
            warning_categories.append(f"{budget.get_category_display()} (Approaching)")

    if warning_categories:
        return "You are exceeding or close to exceeding the following budgets: " + ", ".join(warning_categories)
    else:
        return ""



