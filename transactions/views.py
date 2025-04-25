from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction, BankTransaction
from .forms import TransactionForm
from django.shortcuts import get_object_or_404
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from datetime import datetime, timedelta
from accounts.models import UserProfile
from plaid_client import client

from django.http import JsonResponse
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
from collections import OrderedDict
from analytics.models import GraphGenerationLog
from budgets.models import Budget
from .forms import EmailForm

from django.conf import settings
from django.core.mail import EmailMessage
import json


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            GraphGenerationLog.objects.create(
                user=request.user,
                graph_type='transaction-update'
            )

            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})


@login_required
def transaction_list(request):
    selected_categories = request.GET.getlist('category')

    # Manual entries
    if selected_categories:
        transactions = Transaction.objects.filter(user=request.user, category__in=selected_categories)
    else:
        transactions = Transaction.objects.filter(user=request.user)

    # Plaid-linked entries
    bank_transactions = BankTransaction.objects.filter(user=request.user).order_by('-date')

    context = {
        'transactions': transactions,
        'bank_transactions': bank_transactions,
        'category_choices': [
            ('FOOD', 'Food'),
            ('RENT', 'Rent'),
            ('UTIL', 'Utilities'),
            ('TRAN', 'Transport'),
            ('ENTR', 'Entertainment'),
            ('HEAL', 'Healthcare'),
            ('MISC', 'Miscellaneous'),
        ],
        'selected_categories': selected_categories
    }
    return render(request, 'transactions/transaction_list.html', context)

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})

@login_required

def fetch_bank_transactions(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        access_token = user_profile.access_token

        start_date = (datetime.now() - timedelta(days=30)).date()
        end_date = datetime.now().date()

        request_obj = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date,
            options=TransactionsGetRequestOptions(count=100)
        )

        response = client.transactions_get(request_obj)

        for txn in response['transactions']:
            _, created = BankTransaction.objects.get_or_create(
                user=request.user,
                plaid_transaction_id=txn['transaction_id'],
                defaults={
                    'name': txn['name'],
                    'amount': txn['amount'],
                    'date': txn['date'],
                    'account_name': txn['account_id'],
                    'category': " / ".join(txn.get('category', [])) if txn.get('category') else "",
                    'pending': txn.get('pending', False)
                }
            )

        return redirect('transaction_list')

    except Exception as e:
        print("Error fetching Plaid transactions:", e)
        return redirect('transaction_list')

def user_report_page(request):
    return render(request, 'transactions/report.html')

@login_required
def user_report_data(request):
    user = request.user
    time_range = request.GET.get('range', 'all')

    today = now()

    if time_range == '3months':
        start_date = today - timedelta(days=90)
        transactions = Transaction.objects.filter(user=user, date__gte=start_date)

        # Create monthly buckets for the past 3 months
        monthly_data = OrderedDict()
        for i in range(2, -1, -1):
            month_date = today - timedelta(days=30 * i)
            label = month_date.strftime('%B %Y')
            monthly_data[label] = 0

        for t in transactions:
            if t.date:
                label = t.date.strftime('%B %Y')
                if label in monthly_data:
                    monthly_data[label] += t.amount

    else:  # all time
        transactions = Transaction.objects.filter(user=user)

        # Create monthly buckets for the past 12 months
        monthly_data = OrderedDict()
        for i in range(11, -1, -1):
            month_date = today - timedelta(days=30 * i)
            label = month_date.strftime('%B %Y')
            monthly_data[label] = 0

        for t in transactions:
            if t.date:
                label = t.date.strftime('%B %Y')
                if label in monthly_data:
                    monthly_data[label] += t.amount

    category_data = (
        transactions.values('category')
        .annotate(total=Sum('amount'))
    )

    return JsonResponse({
        'category_data': list(category_data),
        'monthly_data': monthly_data,
    })

@login_required
def report_view(request):
    # Get all the user's transactions and budgets
    transactions = Transaction.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)

    # Calculate total spent per category
    category_totals = {}
    for t in transactions:
        if t.category in category_totals:
            category_totals[t.category] += t.amount
        else:
            category_totals[t.category] = t.amount

    # Generate warnings if any budget is exceeded
    warnings = []
    for budget in budgets:
        spent = category_totals.get(budget.category, 0)
        if spent > budget.amount:
            warnings.append(f"You are exceeding your budget in {budget.category}. Consider reducing spending.")

    email_form = EmailForm()

    context = {
        'transactions': transactions,
        'warnings': warnings,  # pass to report.html
        'form': email_form,
    }
    return render(request, 'transactions/report.html', context)

def send_email(request):
    data = json.loads(request.body)

    user_profile = UserProfile.objects.filter(user=request.user)[0]
    user_name = user_profile.first_name + " " + user_profile.last_name

    subject = f"Financial Report from {user_name}"
    body = f"{user_name}, a MoneyParce user, has shared the attached financial report with you."
    from_email = settings.DEFAULT_FROM_EMAIL

    email_address = data.get('email')
    recipient_list = [email_address]

    email = EmailMessage(
        subject,
        body,
        from_email,
        recipient_list,
    )

    # email.attach(financial_report.pdf)

    email.send()
    return JsonResponse({'success': True, 'message': f'Email notification sent to {email_address}.'})