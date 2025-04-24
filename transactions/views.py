from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, BankTransaction
from .forms import TransactionForm
from django.shortcuts import get_object_or_404
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from datetime import datetime, timedelta
from accounts.models import UserProfile
from plaid_client import client

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
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